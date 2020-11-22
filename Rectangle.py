import arcpy

def main():
    import os

    arcpy.env.overwriteOutput = True

    # input dbf file, edit this !!!
    tbl = r'D:\Xander\GeoNet\DBF2Rectangles\testdata.dbf'

    # edit these field names !!!
    fld_oid_in = 'OID@'
    fld_X = 'X'
    fld_Y = 'Y'
    fld_width = 'Width'
    fld_height = 'Height'
    fld_oid_out = 'OID_DBF'

    # output feature class
    fc_out = r'D:\Xander\GeoNet\DBF2Rectangles\test.gdb\rectangles' # edit this !!!

    # define a spatial reference, edit this !!!
    sr = arcpy.SpatialReference(3857)  # example for WGS_1984_Web_Mercator_Auxiliary_Sphere

    # create output featureclass
    fc_ws, fc_name = os.path.split(fc_out)
    arcpy.CreateFeatureclass_management(fc_ws, fc_name, "POLYGON", None, None, None, sr)

    # add field OID DBF
    AddField(fc_out, fld_oid_out, "LONG", None)

    # insert cursor to store the results
    flds_out = ('SHAPE@', fld_oid_out)
    with arcpy.da.InsertCursor(fc_out, flds_out) as curs_out:

        # loop over dbf file
        flds = (fld_oid_in, fld_X, fld_Y, fld_width, fld_height)
        with arcpy.da.SearchCursor(tbl, flds) as curs:
            for row in curs:
                oid = row[0]
                x = row[1]
                y = row[2]
                w = row[3]
                h = row[4]
                polygon = createRectangle(x, y, w, h, sr)
                curs_out.insertRow((polygon, oid, ))


def AddField(fc, fld_name, fld_type, fld_length):
    if len(arcpy.ListFields(fc, fld_name)) == 0:
        arcpy.AddField_management(fc, fld_name, fld_type, None, None, fld_length)


def createRectangle(x, y, w, h, sr):
    xmin = float(x) - float(w) / 2.0
    xmax = float(x) + float(w) / 2.0
    ymin = float(y) - float(h) / 2.0
    ymax = float(y) + float(h) / 2.0
    lst_pnts = []
    lst_pnts.append(arcpy.Point(xmin, ymin))
    lst_pnts.append(arcpy.Point(xmin, ymax))
    lst_pnts.append(arcpy.Point(xmax, ymax))
    lst_pnts.append(arcpy.Point(xmax, ymin))
    lst_pnts.append(lst_pnts[0])
    return arcpy.Polygon(arcpy.Array(lst_pnts), sr)


if __name__ == '__main__':
    main()