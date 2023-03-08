#-------------------------------------------------------------------------------
# Name:        Eliminar Usuarios del Portal o AGOL a partir de una lista de usuarios
# Purpose:
#
# Author:      osolis
#
# Created:     20/02/2023
# Copyright:   (c) osolis 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from arcgis.gis import GIS
import csv
import arcpy
gis = GIS(arcpy.GetParameterAsText(0), arcpy.GetParameterAsText(1),arcpy.GetParameterAsText(2))
csv_file_path = arcpy.GetParameterAsText(3)
source_items_by_id = {}
administrador=arcpy.GetParameterAsText(1)
with open(csv_file_path) as csv_file_input:
    csv_input = csv.reader(csv_file_input, delimiter=",")
    for row in csv_input:
        arcpy.AddMessage(str(row[0]))

        # Try to find the User with the specified Name. If found, delete the User
        user_by_name = gis.users.get(str(row[0]))

        if user_by_name:
            num_items = 0
            num_folders = 0
            arcpy.AddMessage("Contando los item ids para {}".format(user_by_name.username))
            user_content = user_by_name.items()
            # Get item ids from root folder first
            for item in user_content:
                num_items += 1
                source_items_by_id[item.itemid] = item
            # Get item ids from each of the folders next
            folders = user_by_name.folders
            for folder in folders:
                num_folders += 1
                folder_items = user_by_name.items(folder=folder['title'])
                for item in folder_items:
                    num_items += 1
                    source_items_by_id[item.itemid] = item

            arcpy.AddMessage("Número de carpetas {} # Número de items {}".format(str(num_folders), str(num_items)))
            if num_items > 0:
                arcpy.AddMessage("No Eliminar a: {} todavía".format(user_by_name.username))
                #Reasignar grupos
                olduser = gis.users.get(user_by_name.username)
                usergroups = olduser['groups']
                for group in usergroups:
                    grp = gis.groups.get(group['id'])
                    if (grp.owner == olduser):
                        grp.reassign_to(administrador)
                    else:
                        grp.add_users(administrador)
                        grp.remove_users(olduser)
                #Mover contenido
                usercontent = olduser.items()
                folders = olduser.folders
                for item in usercontent:
                    try:
                        item.reassign_to(administrador)
                    except Exception as e:
                        arcpy.AddMessage("Puede que el Item ya fuera asignado al administrador.")

                for folder in folders:
                    try:
                        gis.content.create_folder(folder['title'], administrador)
                        folderitems = olduser.items(folder=folder['title'])
                        for item in folderitems:
                            item.reassign_to(administrador, target_folder=folder['title'])
                    except Exception as e:
                        arcpy.AddMessage("Puede que el Item ya fuera asignado al administrador.")
                #Eliminar al usuario
                arcpy.AddMessage(" - Eliminando...")
                user_by_name.delete()
            else:
                arcpy.AddMessage("Eliminar a usuario: {}".format(user_by_name.username))
                #Reasignar grupos
                olduser = gis.users.get(user_by_name.username)
                usergroups = olduser['groups']
                for group in usergroups:
                    grp = gis.groups.get(group['id'])
                    if (grp.owner == olduser):
                        grp.reassign_to(administrador)
                    else:
                        grp.add_users(administrador)
                        grp.remove_users(olduser)
                arcpy.AddMessage(" - Eliminando...")
                user_by_name.delete()
##        else:
##            # If user could not be found by name; search by email, and delete if a single member is found.
##            users_by_email = [user for user in gis.users.search() if user.email == str(row[1])]
##            if len(users_by_email) == 1:
##                arcpy.AddMessage(" - Eliminando...")
##                users_by_email[0].delete()
##            elif len(users_by_email) > 1:
##                arcpy.AddMessage(" - Se encontro mas de un usuario con el correo especificado")
        else:
            arcpy.AddMessage(" - No se encuentra un usuario con el nombre o correo especificado")
