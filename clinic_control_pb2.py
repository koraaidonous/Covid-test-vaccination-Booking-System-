# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: clinic_control.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x63linic_control.proto\"*\n\nvacRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06hs_num\x18\x02 \x01(\x05\"\x1b\n\x07vacFile\x12\x10\n\x08vaccines\x18\x01 \x03(\t\"2\n\x12\x61ppointmentRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06hs_num\x18\x02 \x01(\x05\"&\n\x0f\x61ppointmentFile\x12\x13\n\x0b\x61ppointment\x18\x01 \x01(\t\".\n\x0eresultsRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06hs_num\x18\x02 \x01(\x05\"\x1e\n\x0bresultsFile\x12\x0f\n\x07results\x18\x01 \x01(\x05\x32\xa5\x01\n\nClinicCtrl\x12(\n\rgetVacHistory\x12\x0b.vacRequest\x1a\x08.vacFile\"\x00\x12\x39\n\x0egetAppointment\x12\x13.appointmentRequest\x1a\x10.appointmentFile\"\x00\x12\x32\n\x0fgetCovidResults\x12\x0f.resultsRequest\x1a\x0c.resultsFile\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'clinic_control_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _VACREQUEST._serialized_start=24
  _VACREQUEST._serialized_end=66
  _VACFILE._serialized_start=68
  _VACFILE._serialized_end=95
  _APPOINTMENTREQUEST._serialized_start=97
  _APPOINTMENTREQUEST._serialized_end=147
  _APPOINTMENTFILE._serialized_start=149
  _APPOINTMENTFILE._serialized_end=187
  _RESULTSREQUEST._serialized_start=189
  _RESULTSREQUEST._serialized_end=235
  _RESULTSFILE._serialized_start=237
  _RESULTSFILE._serialized_end=267
  _CLINICCTRL._serialized_start=270
  _CLINICCTRL._serialized_end=435
# @@protoc_insertion_point(module_scope)
