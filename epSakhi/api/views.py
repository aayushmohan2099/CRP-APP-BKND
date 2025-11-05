# epSakhi/api/views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from epSakhi.models import CRPEP, BeneficiaryEnterprise
from core.models import MasterPanchayat, MasterShgList, MasterVillage, MasterBeneficiary, MasterDistrict, MasterBlock
from .serializers import CRPEPSerializer, BeneficiaryEnterpriseSerializer, MasterPanchayatSerializer, MasterShgSerializer, MasterBeneficiarySerializer, MasterDistrictSerializer, MasterBlockSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import StreamingHttpResponse
import csv
from io import StringIO

CACHE_TTL = 30  # seconds for hot lists (you asked default)

class CRPEPViewSet(viewsets.ModelViewSet):
    """
    CRUD for CRP-EP (BMMU can create; CRP can view/edit their own)
    """
    queryset = CRPEP.objects.all()
    serializer_class = CRPEPSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name','mobile_number']
    ordering_fields = ['id','created_at']

    def get_queryset(self):
        qs = CRPEP.objects.all().order_by('-id')
        # if user is CRP role, restrict to their own record (master_user link)
        user = self.request.user
        # we have mirror Django user; find master_user by username
        from core.models import MasterUser
        try:
            mu = MasterUser.objects.using('master').get(username=user.username)
            if mu.role == 'crp_ep':
                qs = qs.filter(master_user_id=mu.id)
        except Exception:
            pass
        return qs

    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(CACHE_TTL))
    def mylist(self, request):
        """Fast list for logged-in CRP or BMMU (cached)"""
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = CRPEPSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CRPEPSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export CRP rows created by logged-in BMMU (or all for admin) - returns CSV stream"""
        qs = self.get_queryset()
        # build CSV
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(['id','name','district_id','block_id','panchayat_id','shg_code','mobile_number','category','marks_obtained'])
        for r in qs:
            writer.writerow([r.id, r.name, r.district_id, r.block_id, r.gram_panchayat_id, getattr(r, 'shg_id', ''), r.mobile_number, r.category, r.marks_obtained])
        buffer.seek(0)
        response = StreamingHttpResponse(buffer, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="crpep_export.csv"'
        return response

class CRPPanchayatMappingViewSet(viewsets.ViewSet):
    """
    Link panchayats to CRP-EP
    """
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def link(self, request, pk=None):
        """link panchayats list to CRP id"""
        crp_id = pk
        panchayat_ids = request.data.get('panchayat_ids', [])
        if not isinstance(panchayat_ids, list):
            return Response({'detail':'panchayat_ids must be list'}, status=status.HTTP_400_BAD_REQUEST)
        # create CRPEPToPanchayat model if exists; alternatively store comma. We'll assume separate mapping model exists.
        from epSakhi.models import CRPEPToPanchayat
        created = []
        with transaction.atomic():
            for pid in panchayat_ids:
                obj, _ = CRPEPToPanchayat.objects.get_or_create(crp_id=crp_id, allocated_panchayat_id=pid)
                created.append(obj.id)
        return Response({'created_ids': created})

class BeneficiaryEnterpriseViewSet(viewsets.ModelViewSet):
    queryset = BeneficiaryEnterprise.objects.all().order_by('-id')
    serializer_class = BeneficiaryEnterpriseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['enterprise_name','main_product_service']
    ordering_fields = ['id','created_at']

    def get_queryset(self):
        qs = BeneficiaryEnterprise.objects.select_related('recorded_by_user').all().order_by('-id')
        # If CRP, restrict to their recorded_by_user entries or CRP coverage: We'll restrict to recorded_by_user or crp mapping:
        user = self.request.user
        from core.models import MasterUser
        try:
            mu = MasterUser.objects.using('master').get(username=user.username)
            if mu.role == 'crp_ep':
                qs = qs.filter(recorded_by_user_id=mu.id)
        except Exception:
            pass
        return qs
