from rest_framework.pagination import PageNumberPagination

class MpcProductPagination(PageNumberPagination):
    """
    Custom pagination for the MPC product catalog.
    Returns 30 items per page by default.
    """
    page_size = 30

    # This allow frontend to request a different amount of products if needed
    page_size_query_param = 'page_size' 
    
    #This prevent malicious user from requesting more products that can crash server
    max_page_size = 100