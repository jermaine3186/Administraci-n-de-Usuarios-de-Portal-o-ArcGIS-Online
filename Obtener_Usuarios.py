#-------------------------------------------------------------------------------
# Name:        Revisar los usuarios del portal y obtener la última fecha en la que se loguearon o si se han logueado
# Purpose:
#
# Author:      osolis
#
# Created:     20/02/2023
# Copyright:   (c) osolis 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcgis
import time
from arcgis.gis import GIS
import arcpy
ago_gis = GIS(arcpy.GetParameterAsText(0), arcpy.GetParameterAsText(1),arcpy.GetParameterAsText(2))
a_users = ago_gis.users.search('!esri_ & !admin', max_users=2000)
archivocsv=arcpy.GetParameterAsText(3)
arcpy.AddMessage("Creando csv con los datos de los usuarios del portal o ArcGIS Online")
f=open(archivocsv,"a+")
for i in range(1):
    f.write("Nombre,usuario,Nivel,Rol,Ultima actividad,Fecha ultima actividad"+"\n")
f.close()
arcpy.AddMessage("Revisando usuarios")
for a_user in a_users:
    if a_user. lastLogin != -1:
        last_accessed = time.localtime(a_user. lastLogin/1000)
        f=open(archivocsv,"a+")
        for i in range(1):
            f.write(str(a_user. fullName)+","+str(a_user. username)+","+(a_user.level)+","+(a_user.role) + ",{}/{}/{}".format(last_accessed[2], last_accessed[1], last_accessed[0])+ ",{}/{}/{}".format(last_accessed[2], last_accessed[1], last_accessed[0])+"\n")
        f.close()
    else:
        f=open(archivocsv,"a+")
        for i in range(1):
            f.write(str(a_user. fullName)+","+str(a_user. username)+","+(a_user.level)+","+(a_user.role) + ",nunca ha iniciado sesión."+"\n")
        f.close()
arcpy.AddMessage("Revisión de usuarios y creación de csv completada exitosamente")