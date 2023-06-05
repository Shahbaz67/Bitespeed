from rest_framework import viewsets
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer
from .config import get_itentify_response, combine_customers

class ContactViewSet(viewsets.ModelViewSet):
    """
    Contact ViewSet
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email=request.data.get('email')
        phone_number=request.data.get('phone_number')
        if (not email and not phone_number):
            return Response("Please enter either email or phone_number", status=404)

        # Deal separately for request with email or phone_number being null or not
        if email and not phone_number:
            # Request phone_number is null, check if email exists, return consolidated contact otherwise create a new contact
            check_email = Contact.objects.filter(email=email).exists()
            if check_email:
                email_instance = Contact.objects.filter(email=email).first()
                p_id = email_instance.linked_id_id if email_instance.link_precedence == "secondary" else email_instance.id
                response = get_itentify_response(p_id)
                return Response(response, status=200)
            else:
                self.perform_create(serializer)
                return Response(serializer.data)
            

        elif not email and phone_number:
            # Request email is null, check if phone_number exists, return consolidated response otherwise create a new contact
            check_phone = Contact.objects.filter(phone_number=phone_number).exists()
            if check_phone:
                phone_instance = Contact.objects.filter(phone_number=phone_number).first()
                p_id = phone_instance.linked_id_id if phone_instance.link_precedence == "secondary" else phone_instance.id
                response = get_itentify_response(p_id)
                return Response(response, status=200)
            else:
                self.perform_create(serializer)
                return Response(serializer.data)
        else:
            # Request contain both email and phone_number
            # 3 possibilities: both email and phone_number already exists, or one of them exists or none exists
            check_email = Contact.objects.filter(email=email).exists()
            check_phone = Contact.objects.filter(phone_number=phone_number).exists()

            if check_email and check_phone:
                # both email and phone_number already exists
                check_email_phone = Contact.objects.filter(email=email, phone_number=phone_number).exists()
                if check_email_phone:
                    email_phone_instance = Contact.objects.get(email=email, phone_number=phone_number)
                    p_id = email_phone_instance.linked_id_id if email_phone_instance.link_precedence == "secondary" else email_phone_instance.id
                    response = get_itentify_response(p_id)
                    return Response(response, status=200)
                else:
                    p_id = combine_customers(email, phone_number)
                    response = get_itentify_response(p_id)
                    return Response(response, status=200)       

            if (not check_email and check_phone) or (check_email and not check_phone):
                # Either email or phone_number exists
                if check_email:
                    email_instance = Contact.objects.filter(email=email).first()
                    p_id = email_instance.linked_id_id if email_instance.link_precedence == "secondary" else email_instance.id
                    request.data["linked_id"] = p_id
                if check_phone:
                    phone_instance = Contact.objects.filter(phone_number=phone_number).first()
                    p_id = phone_instance.linked_id_id if phone_instance.link_precedence == "secondary" else phone_instance.id
                    request.data["linked_id"] = p_id
                request.data["link_precedence"] = "secondary"
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)

