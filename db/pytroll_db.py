import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime,\
                       create_engine, ForeignKey, Table

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, backref, sessionmaker


#from osgeo import ogr
import shapely.wkb
import shapely.wkt

from sqltypes import LINESTRING, POLYGON

Base = declarative_base()

#relation table
data_boundary = Table('data_boundary', Base.metadata,\
                      Column('filename', String,\
                             ForeignKey('file.filename')),\
                      Column('boundary_id', Integer,\
                             ForeignKey('boundary.boundary_id')))

#relation table
file_type_parameter = Table('file_type_parameter', Base.metadata,\
                      Column('file_type_id', Integer,\
                             ForeignKey('file_type.file_type_id')),\
                      Column('parameter_id', Integer,\
                             ForeignKey('parameter.parameter_id')))

#relation table
file_tag = Table('file_tag', Base.metadata,\
                      Column('tag_id', Integer,\
                             ForeignKey('tag.tag_id')),\
                      Column('filename', String,\
                             ForeignKey('file.filename')))

#relation table
file_type_tag = Table('file_type_tag', Base.metadata,\
                      Column('tag_id', Integer,\
                             ForeignKey('tag.tag_id')),\
                      Column('file_type_id', Integer,\
                             ForeignKey('file_type.file_type_id')))

        

class ParameterType(Base):
    __tablename__ = 'parameter_type'

    #mapping
    parameter_type_id = Column(Integer, primary_key=True)
    parameter_type_name = Column(String)
    parameter_location = Column(String)
    

    def __init__(self, parameter_type, parameter_type_name, parameter_location):
        self.parameter_type = parameter_type
        self.parameter_type_name = parameter_type_name
        self.parameter_location = parameter_location


class Parameter(Base):
    __tablename__ = 'parameter'

    #mapping
    parameter_id = Column(Integer, primary_key=True)
    parameter_type_id = Column(Integer, ForeignKey('parameter_type.parameter_type_id'))
    parameter_name = Column(String)
    description = Column(String)
    
    def __init__(self, parameter_id, parameter_type_id, parameter_name, description):
        self.parameter_id = parameter_id
        self.parameter_type_id = parameter_type_id
        self.parameter_name = parameter_name
        self.description = description


class Tag(Base):
    __tablename__ = 'tag'

    #mapping
    tag_id = Column(Integer, primary_key=True)
    tag = Column(String)

    def __init__(self,tag_id, tag):
        self.tag_id = tag_id
        self.tag = tag


class FileFormat(Base):
    __tablename__ = 'file_format'

    #mapping
    file_format_id = Column(Integer, primary_key=True)
    file_format_name = Column(String)
    description = Column(String)
    
    def __init__(self,file_format_id, file_format_name, description):
        self.file_format_id = file_format_id
        self.file_format_name = file_format_name
        self.description = description



class FileType(Base):
    __tablename__ = 'file_type'

    #mapping
    file_type_id = Column(Integer, primary_key=True)
    file_type_name = Column(String)
    description = Column(String)

    def __init__(self, file_type_id, file_type_name, description):
        self.file_type_id = file_type_id
        self.file_type_name = file_type_name
        self.description = description

'''
class FileTypeParameter(Base):
    __tablename__ = 'file_type_parameter'

    #mapping
    file_type_id = Column(Integer, ForeignKey('file_type.file_type_id'), primary_key=True)
    parameter_id = Column(Integer, ForeignKey('parameter.parameter_id'), primary_key=True)

    #relations

    FileTypeParameter.file_type = relation(FileType)
    FileTypeParameter.parameter = relation(Parameter)

    def __init__(self, file_type_id, parameter_id):
        self.file_type_id = file_type_id
        self.parameter_id = parameter_id
'''

class File(Base):
    __tablename__ = 'file'

    #mapping
    filename = Column(String, primary_key=True)
    file_type_id = Column(Integer, ForeignKey('file_type.file_type_id'))
    file_format_id = Column(Integer, ForeignKey('file_format.file_format_id'))
    is_archived = Column(Boolean)
    creation_time = Column(DateTime)
    
    def __init__(self, filename, file_type, file_format, is_archived, creation_time):
        self.filename = filename
        self.file_type = file_type
        self.file_format = file_format
        self.is_archived = is_archived
        self.creation_time = creation_time


class Boundary(Base):
    __tablename__ = 'boundary'

    #mapping
    boundary_id = Column(Integer, primary_key=True)
    boundary_name = Column(String)
    boundary = Column(POLYGON())    
    creation_time = Column(DateTime)
    
    def __init__(self, boundary_id, boundary_name, boundary, creation_time=None):
        self.boundary_id = boundary_id
        self.boundary_name = boundary_name
        self.boundary = boundary
        if creation_time is None:
            creation_time = datetime.datetime.utcnow()
        self.creation_time = creation_time

'''
class DataBoundary(Base):
    __tablename__ = 'data_boundary'

    #mapping
    filename = Column(String, ForeignKey('file.filename'), primary_key=True)
    boundary_id = Column(Integer, ForeignKey('boundary.boundary_id'), primary_key=True)
    creation_time = Column(DateTime)


    #relations
    """file_obj = relation(File)
    boundary = relation(Boundary)"""

    def __init__(self, filename, boundary_id, creation_time):
        self.filename = filename
        self.boundary_id = boundary_id
        self.creation_time = creation_time
'''

class ParameterLinestring(Base):
    __tablename__ = 'parameter_linestring'

    #mapping
    filename = Column(String, ForeignKey('file.filename'), primary_key=True)
    parameter_id = Column(Integer, ForeignKey('parameter.parameter_id'), primary_key=True)
    creation_time = Column(DateTime)
    data_value = Column(LINESTRING())

    def __init__(self, file_obj, parameter, creation_time, data_value):
        self.file_obj = file_obj
        self.parameter = parameter
        self.creation_time = creation_time
        self.data_value = data_value


class ParameterValue(Base):
    __tablename__ = "parameter_value"

    #mapping
    filename = Column(String, ForeignKey('file.filename'), primary_key=True)
    parameter_id = Column(Integer, ForeignKey('parameter.parameter_id'), primary_key=True)
    data_value = Column(String)
    creation_time = Column(DateTime)

    def __init__(self, file_obj, parameter, data_value, creation_time):
        self.file_obj = file_obj
        self.parameter = parameter
        self.creation_time = creation_time
        self.data_value = data_value


'''
class FileTag(Base):
    __tablename__ = "file_tag"

    #mapping
    tag_id = Column(Integer, ForeignKey('tag.tag_id'), primary_key=True)
    filename = Column(String, ForeignKey('file.filename'), primary_key=True)
    creation_time = Column(DateTime)

    #relations
    tag = relation(Tag)
    file_obj = relation(File)

    def __init__(self, tag_id, filename, creation_time):
        self.tag_id = tag_id
        self.filename = filename
        self.creation_time = creation_time
'''

class FileURI(Base):
    __tablename__ = "file_uri"

    #mapping
    file_type_id = Column(Integer, ForeignKey('file_type.file_type_id'), primary_key=True)
    file_format_id = Column(Integer, ForeignKey('file_format.file_format_id'), primary_key=True)
    sequence = Column(Integer, primary_key=True)
    uri = Column(String, primary_key=True)
    
    def __init__(self, file_type, file_format, sequence, uri):
        self.file_type = file_type
        self.file_format = file_format
        self.sequence = sequence
        self.uri = uri

'''
class FileTypeTag(Base):
    __tablename__ = "file_type_tag"

    #mapping
    tag_id = Column(Integer, ForeignKey('tag.tag_id'), primary_key=True)
    file_type_id = Column(Integer, ForeignKey('file_type.file_type_id'), primary_key=True)
    creation_time = Column(DateTime)

    #relations
    """tag = relation(Tag)
    file_type = relation(FileType)"""

    def __init__(self, tag_id, file_type_id, creation_time):
        self.tag_id = tag_id
        self.file_type_id = file_type_id
        self.creation_time
'''



#
#relations

#ParameterType
ParameterType.parameters = relation(Parameter)

#Parameter
Parameter.parameter_type = relation(ParameterType)
Parameter.parameter_values = relation(ParameterValue)
Parameter.parameter_linestrings = relation(ParameterLinestring)
Parameter.file_types = relation(FileType, secondary=file_type_parameter)

#Tag
Tag.files = relation(File, secondary=file_tag)
Tag.file_types = relation(FileType, secondary=file_type_tag)

#FileFormat
FileFormat.file_uris = relation(FileURI)
FileFormat.file_objs = relation(File)

#FileType
FileType.parameters = relation(Parameter, secondary=file_type_parameter)
FileType.file_uris = relation(FileURI)
FileType.file_objs = relation(File)
FileType.file_type_tags = relation(Tag, secondary=file_type_tag)

#Boundary
Boundary.files = relation(File, secondary=data_boundary)

#File
File.file_type = relation(FileType)
File.file_format = relation(FileFormat)
File.parameter_values = relation(ParameterValue)
File.parameter_linestrings = relation(ParameterLinestring)
File.file_tags = relation(Tag, secondary=file_tag)
File.boundary = relation(Boundary, secondary=data_boundary)

#ParameterLinestring
ParameterLinestring.file_obj = relation(File)
ParameterLinestring.parameter = relation(Parameter)

#ParameterValue
ParameterValue.file_obj = relation(File)
ParameterValue.parameter = relation(Parameter)

#FileURI
FileURI.file_type = relation(FileType)
FileURI.file_format = relation(FileFormat)


class DCManager(object):
    """Data Center Manager
    """

    def __init__(self, connection_string):
        engine = create_engine(connection_string)
        self._engine = engine
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def save(self):
        try:
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def create_file_type(self, file_type_id, file_type_name, description):
        file_type = FileType(file_type_id, file_type_name, description)
        self._session.add(file_type)
        return file_type

    def create_file_format(self, file_format_id, file_format_name, description):
        file_format = FileFormat(file_format_id, file_format_name, description)
        self._session.add(file_format)
        return file_format

    def create_file_uri(self, file_type, file_format, URI, sequence=1):
        file_uri = FileURI(file_type, file_format, URI, sequence)
        self._session.add(file_uri)
        return file_uri

    def create_file(self, filename, file_type, file_format, is_archived=False, creation_time=None):
        if creation_time is None:
            creation_time = datetime.datetime.utcnow()            
        file_obj = File(filename, file_type, file_format, is_archived, creation_time)
        self._session.add(file_obj)
        return file_obj

    def create_parameter_type(self, parameter_type_id, parameter_type_name, parameter_location):
        parameter_type = ParameterType(parameter_type_id, parameter_type_name, parameter_location)
        self._session.add(parameter_type)
        return parameter_type

    def create_parameter(self, parameter_id, parameter_type, parameter_name, description):
        parameter = Parameter(parameter_id, parameter_type, parameter_name, description)
        self._session.add(parameter)
        return parameter

    def create_parameter_value(self, file_obj, parameter, data_value, creation_time=None):
        if creation_time is None:
            creation_time = datetime.datetime.utcnow()
        parameter_value = ParameterValue(file_obj, parameter, data_value, creation_time)         
        self._session.add(parameter_value)
        return parameter_value

    def create_parameter_linestring(self, file_obj, parameter, data_value, creation_time=None):
        if creation_time is None:
            creation_time = datetime.datetime.utcnow()
        parameter_linestring = ParameterLinestring(file_obj, parameter, data_value, creation_time)         
        self._session.add(parameter_linestring)
        return parameter_linestring

    def create_boundary(self, boundary_id, boundary_name, boundary, creation_time=None):
        if creation_time is None:
            creation_time = datetime.datetime.utcnow()
        boundary_obj = Boundary(boundary_id, boundary_name, boundary, creation_time)         
        self._session.add(boundary_obj)
        return boundary_obj

    def create_tag(self, tag_id, tag):
        tag_obj = Tag(tag_id, tag)
        self._session.add(tag_obj)
        return tag_obj

    def get_file_type(self, file_type_name):
        return self._session.query(FileType).\
               filter(FileType.file_type_name == file_type_name).one()

    def get_file_format(self, file_format_name):
        return self._session.query(FileFormat).\
               filter(FileFormat.file_format_name == file_format_name).one()

    def get_parameter(self, parameter_name):
        return self._session.query(Parameter).\
               filter(Parameter.parameter_name == parameter_name).one()


class ReportManager(object):

    def __init__(self, connection_string):
        engine = create_engine(connection_string)
        self._engine = engine
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def get_file(self):
        return self._session.query(File).first()

    def get_param_track(self):
        #query = 'select filename, parameter_id from parameter_track';
        #data_proxy = self._engine.execute(query)
        #print data_proxy.fetchall()
        return  self._session.query(ParameterLinestring)

    def add_param_track(self):
        line_s = 'LINESTRING (3 1, 4 4, 5 5, 5 6)'
        wkt_o = shapely.wkt.loads(line_s)
        print wkt_o
        wkb_o = wkt_o.wkb #shapely.wkb.dumps(wkt_o)
        

        #print type(wkb_o)
        #param_track = ParameterLinestring("hrpt_201012011615_lvl0_smb.l0", 8, datetime.datetime.utcnow(), wkb_o.encode('hex'))
        #param_track = ParameterLinestring("hrpt_201012011615_lvl0_smb.l0", 8, datetime.datetime.utcnow(), wkt_o)
        #self._session.add(param_track)
        self._session.commit()


if __name__ == '__main__':
    rm = ReportManager('postgresql://iceopr:Hot_Eyes@devsat-lucid:5432/testdb2')
    f = rm.get_file()
    pl = f.parameter_linestrings[0]
    print type(pl.data_value)
    print pl.data_value.wkt
    #pt = rm.get_param_track()
    #res = pt.first()
    #print type(res.data_value)
    #t_geo = ogr.CreateGeometryFromWkb(res.track.decode('hex'))
    #t_geo = shapely.wkb.loads(res.data_value.decode('hex')).wkt
    #t_geo = res.data_value.wkt    

    #print res.filename, res.parameter_id, res.creation_time, t_geo
    
    # insert into database
    #rm.add_param_track()
    #pt = rm.get_param_track()
    #res = pt.first()
    
    





