from sqlalchemy import null

address = [
    {
        "buildingnumber": "0014",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    },
    {
        "buildingnumber": "0015",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    },
    {
        "buildingnumber": "0016",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    },
    {
        "buildingnumber": "0018",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    },
    {
        "buildingnumber": "0020",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    },
    {
        "buildingnumber": "0021",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    },
    {
        "buildingnumber": "0022",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    },
    {
        "buildingnumber": "0023",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    },
    {
        "buildingnumber": "0025",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    },
    {
        "buildingnumber": "0027",
        "buildingname": null,
        "thoroughfarename": "GUILDFORD",
        "thoroughfaredescriptor": "DRIVE",
        "posttown": "GLASGOW",
        "dependentlocality": ""
    }
]

tmp_dict = {}
final_address = []

for i in range(len(address)):
    # Taking first dict from the list and looping through that
    tmp_dict = address[i]
    # Looping through the vals in tmp_dict and adding them to a new list
    pulled_address = [tmp_dict[v] for v in tmp_dict if type(tmp_dict[v]) != type(null)]
    # Check to see if the first item (building number) starts with 0
    tmp_building_num = pulled_address[0]
    if tmp_building_num.startswith('000'):
        pulled_address[0] = tmp_building_num[3:]
    elif tmp_building_num.startswith('00'):
        pulled_address[0] = tmp_building_num[2:]
    elif tmp_building_num.startswith('0'):
        pulled_address[0] = tmp_building_num[1:]
    # Concatenate string to make a single address string
    res = ' '.join(pulled_address)
    # Insert new string into final_list
    final_address.insert(i, res)
    # Clear the tmp_dict
    tmp_dict.clear()
    # Clear res
    res = ''


for i in final_address:
    print(i)

