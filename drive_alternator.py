from ULCDTinterface.modelers import *
from django.db import connection


default_value = Manufacturers.objects.get_or_create(manufacturer_name='')[0]

first_statements = [
'''CREATE TABLE `Physical_interfaces` (
  `interface_id` int(11) NOT NULL AUTO_INCREMENT,
  `interface_name` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`interface_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Physical_interfaces (`interface_name`) values ('');''',

'''CREATE TABLE `Drive_types` (
  `type_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_types (type_name) values ('');''',

'''CREATE TABLE `Drive_notes` (
  `note_id` int(11) NOT NULL AUTO_INCREMENT,
  `note_text` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`note_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_notes (note_text) values ('');''',

'''CREATE TABLE `Drive_family` (
  `family_id` int(11) NOT NULL AUTO_INCREMENT,
  `family_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`family_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_family (family_name) values ('');''',

'''CREATE TABLE `Drive_width` (
  `width_id` int(11) NOT NULL AUTO_INCREMENT,
  `width_name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`width_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_width (width_name) values ('');''',

'''CREATE TABLE `Drive_height` (
  `height_id` int(11) NOT NULL AUTO_INCREMENT,
  `height_name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`height_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_height (height_name) values ('');''',

'''CREATE TABLE `Drive_length` (
  `length_id` int(11) NOT NULL AUTO_INCREMENT,
  `length_name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`length_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_length (length_name) values ('');''',

'''CREATE TABLE `Drive_weight` (
  `weight_id` int(11) NOT NULL AUTO_INCREMENT,
  `weight_name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`weight_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_weight (weight_name) values ('');''',

'''CREATE TABLE `Drive_power_spin` (
  `power_spin_id` int(11) NOT NULL AUTO_INCREMENT,
  `power_spin_name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`power_spin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_power_spin (power_spin_name) values ('');''',

'''CREATE TABLE `Drive_power_seek` (
  `power_seek_id` int(11) NOT NULL AUTO_INCREMENT,
  `power_seek_name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`power_seek_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_power_seek (power_seek_name) values ('');''',

'''CREATE TABLE `Drive_power_idle` (
  `power_idle_id` int(11) NOT NULL AUTO_INCREMENT,
  `power_idle_name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`power_idle_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_power_idle (power_idle_name) values ('');''',

'''CREATE TABLE `Drive_power_standby` (
  `power_standby_id` int(11) NOT NULL AUTO_INCREMENT,
  `power_standby_name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`power_standby_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Drive_power_standby (power_standby_name) values ('');''',

'''CREATE TABLE `Origins` (
  `origin_id` int(11) NOT NULL AUTO_INCREMENT,
  `origin_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`origin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

'''Insert into Origins (origin_name) values ('');''',

'''alter table Drives
add column `f_manufacturer` int(11) DEFAULT {0};'''.format(default_value.id_manufacturer),
'''alter table Drives
add CONSTRAINT `Drives_Manufacturers_FK` FOREIGN KEY (`f_manufacturer`) REFERENCES `Manufacturers` (`id_manufacturer`);''',

'''alter table Drives
add column `f_interface_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Physical_interfaces_FK` FOREIGN KEY (`f_interface_id`) REFERENCES `Physical_interfaces` (`interface_id`);''',

'''alter table Drives
add column `description` text DEFAULT '';''',

'''alter table Drives
add column `f_type_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_types_FK` FOREIGN KEY (`f_type_id`) REFERENCES `Drive_types` (`type_id`);''',

'''alter table Drives
add column `f_note_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_notes_FK` FOREIGN KEY (`f_note_id`) REFERENCES `Drive_notes` (`note_id`);''',

'''alter table Drives
add column `f_family_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_family_FK` FOREIGN KEY (`f_family_id`) REFERENCES `Drive_family` (`family_id`);''',

'''alter table Drives
add column `f_width_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_width_FK` FOREIGN KEY (`f_width_id`) REFERENCES `Drive_width` (`width_id`);''',

'''alter table Drives
add column `f_height_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_height_FK` FOREIGN KEY (`f_height_id`) REFERENCES `Drive_height` (`height_id`);''',

'''alter table Drives
add column `f_length_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_length_FK` FOREIGN KEY (`f_length_id`) REFERENCES `Drive_length` (`length_id`);''',

'''alter table Drives
add column `f_weight_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_weight_FK` FOREIGN KEY (`f_weight_id`) REFERENCES `Drive_weight` (`weight_id`);''',

'''alter table Drives
add column `f_power_spin_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_power_spin_FK` FOREIGN KEY (`f_power_spin_id`) REFERENCES `Drive_power_spin` (`power_spin_id`);''',

'''alter table Drives
add column `f_power_seek_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_power_seek_FK` FOREIGN KEY (`f_power_seek_id`) REFERENCES `Drive_power_seek` (`power_seek_id`);''',

'''alter table Drives
add column `f_power_idle_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_power_idle_FK` FOREIGN KEY (`f_power_idle_id`) REFERENCES `Drive_power_idle` (`power_idle_id`);''',

'''alter table Drives
add column `f_power_standby_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Drive_power_standby_FK` FOREIGN KEY (`f_power_standby_id`) REFERENCES `Drive_power_standby` (`power_standby_id`);''',

'''alter table Drives
add column `total_writes` varchar(25) DEFAULT '';''',

'''alter table Drives
add column `f_origin_id` int(11) DEFAULT 1;''',
'''alter table Drives
add CONSTRAINT `Drives_Origins_FK` FOREIGN KEY (`f_origin_id`) REFERENCES `Origins` (`origin_id`);''',

'''ALTER TABLE sopena_computers.Drives ADD date_added DATE DEFAULT '2000-01-01' NOT NULL;''',

'''UPDATE Speed
set speed_name = REPLACE(speed_name, 'HDD | ', '');''',

'''UPDATE Speed
set speed_name = REPLACE(speed_name, ' RPM', '');''',

'''UPDATE Speed
set speed_name = REPLACE(speed_name, 'Unknown', '0');''',

'''update Form_factor
set Form_factor_name = REPLACE(Form_factor_name, '"', '');''',
]


with connection.cursor() as cursor:
    for statement in first_statements:
        print(statement)
        cursor.execute(statement)


ssd_speed_keywords = ['SSD', 'eMMC/MMC', '']
for drive in Drives.objects.all():
    if drive.f_speed.speed_name in ssd_speed_keywords:
        drive.f_type = DriveTypes.objects.get_or_create(type_name='SSD')[0]
        drive.f_speed = Speed.objects.get_or_create(speed_name=0)[0]
    else:
        drive.f_type = DriveTypes.objects.get_or_create(type_name='HDD')[0]
    drive.save()

Speed.objects.get(speed_name='SSD').delete()
Speed.objects.get(speed_name='eMMC/MMC').delete()
Speed.objects.get(speed_name='').delete()
Speed.objects.get(speed_id=3).delete()
