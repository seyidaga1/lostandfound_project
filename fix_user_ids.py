# fix_user_ids.py
import json
import uuid

def fix_user_ids_in_json(input_file, output_file):
    """Convert UUID user IDs to integers"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    uuid_to_int = {}  # Map UUIDs to sequential integers
    next_id = 1
    
    # First pass: identify all unique user UUIDs
    for item in data:
        if item['model'] == 'accounts.user':
            uuid_pk = item['pk']
            if uuid_pk not in uuid_to_int:
                uuid_to_int[uuid_pk] = next_id
                next_id += 1
    
    # Second pass: replace UUIDs with integers
    for item in data:
        # Fix primary keys for users
        if item['model'] == 'accounts.user':
            old_pk = item['pk']
            item['pk'] = uuid_to_int[old_pk]
        
        # Fix foreign key references to users
        if 'fields' in item:
            fields = item['fields']
            
            # Check common user reference field names
            user_fields = ['user', 'owner', 'created_by', 'updated_by']
            
            for field_name in user_fields:
                if field_name in fields:
                    user_uuid = fields[field_name]
                    if user_uuid in uuid_to_int:
                        fields[field_name] = uuid_to_int[user_uuid]
    
    # Save fixed data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Fixed {len(uuid_to_int)} user IDs")
    print(f"UUID to Integer mapping: {uuid_to_int}")

if __name__ == "__main__":
    fix_user_ids_in_json('datadump.json', 'datadump_fixed_ids.json')