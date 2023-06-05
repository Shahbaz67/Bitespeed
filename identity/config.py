from .models import Contact

def get_itentify_response(id):
    """
    Get the consolidated contacts for customer whose primaryID is "id"
    """
    primary_instance = Contact.objects.get(id=id)
    email_list = []
    phone_list = []
    sec_contact_ids = []

    # Append email and phone_number of primary contact first
    if primary_instance.email:
        email_list.append(primary_instance.email)
    if primary_instance.phone_number:
        phone_list.append(primary_instance.phone_number)
    
    # Iterate through all the linked contacts to this primary instance with id=id
    queryset = Contact.objects.filter(linked_id=id)
    for instance in queryset:
        sec_contact_ids.append(instance.id)
        if instance.email:
            if instance.email not in email_list:
                email_list.append(instance.email)
        if instance.phone_number:
            if instance.phone_number not in phone_list:
                phone_list.append(instance.phone_number)
    response = {
        "contact":{
            "primaryContatctId": id,
            "emails": email_list,
            "phoneNumbers": phone_list,
            "secondaryContactIds": sec_contact_ids
        }
    }
    return response

def combine(old_id, new_id):
    """
    Link all the new_id contacts to old_id
    """
    queryset = Contact.objects.filter(linked_id=new_id)
    for instance in queryset:
        instance.linked_id_id = old_id
        instance.save()
    parent_instance = Contact.objects.get(id=new_id)
    parent_instance.linked_id_id = old_id
    parent_instance.link_precedence = "secondary"
    parent_instance.save()

def combine_customers(email, phone_number):
    """
    Combine two different customers using email of one customer with phone_number of other and return older instance
    """
    email_instance = Contact.objects.filter(email=email).first()
    phone_instance = Contact.objects.filter(phone_number=phone_number).first()

    # Get the primary contact for both the instances
    primary_email_instance_id = email_instance.id
    primary_phone_instance_id = phone_instance.id
    
    if email_instance.link_precedence == "secondary":
        primary_email_instance_id = email_instance.linked_id_id
    if phone_instance.link_precedence == "secondary":
        primary_phone_instance_id = phone_instance.linked_id_id

    # combine contacts if primary contacts of above instances differ
    old_instance_id = primary_email_instance_id
    if primary_email_instance_id == primary_phone_instance_id:
        pass
    elif primary_email_instance_id < primary_phone_instance_id:
        combine(primary_email_instance_id, primary_phone_instance_id)
    else:
        combine(primary_phone_instance_id, primary_email_instance_id)
        old_instance_id = primary_phone_instance_id
    return old_instance_id