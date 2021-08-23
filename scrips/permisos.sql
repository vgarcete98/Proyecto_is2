"""Permisos otorgados al super user de id=1"""

INSERT INTO usuarios_usuario_user_permissions VALUES (1,1,1);
INSERT INTO usuarios_usuario_user_permissions VALUES (2,1,2);
INSERT INTO usuarios_usuario_user_permissions VALUES (3,1,3);
INSERT INTO usuarios_usuario_user_permissions VALUES (4,1,4);
INSERT INTO usuarios_usuario_user_permissions VALUES (5,1,5);
INSERT INTO usuarios_usuario_user_permissions VALUES (6,1,6);
INSERT INTO usuarios_usuario_user_permissions VALUES (7,1,7);
INSERT INTO usuarios_usuario_user_permissions VALUES (8,1,8);
INSERT INTO usuarios_usuario_user_permissions VALUES (9,1,9);
INSERT INTO usuarios_usuario_user_permissions VALUES (10,1,10);
INSERT INTO usuarios_usuario_user_permissions VALUES (11,1,11);
INSERT INTO usuarios_usuario_user_permissions VALUES (12,1,12);
INSERT INTO usuarios_usuario_user_permissions VALUES (13,1,13);
INSERT INTO usuarios_usuario_user_permissions VALUES (14,1,14);
INSERT INTO usuarios_usuario_user_permissions VALUES (15,1,15);
INSERT INTO usuarios_usuario_user_permissions VALUES (16,1,16);
INSERT INTO usuarios_usuario_user_permissions VALUES (17,1,17);
INSERT INTO usuarios_usuario_user_permissions VALUES (18,1,18);
INSERT INTO usuarios_usuario_user_permissions VALUES (19,1,19);
INSERT INTO usuarios_usuario_user_permissions VALUES (20,1,10);
INSERT INTO usuarios_usuario_user_permissions VALUES (21,1,21);
INSERT INTO usuarios_usuario_user_permissions VALUES (22,1,22);
INSERT INTO usuarios_usuario_user_permissions VALUES (23,1,23);
INSERT INTO usuarios_usuario_user_permissions VALUES (24,1,24);
INSERT INTO usuarios_usuario_user_permissions VALUES (25,1,25);

----------TABLA ROL_PERMISOS------------
INSERT INTO rol_permiso VALUES (1,"Crear Usuarios",1);
INSERT INTO rol_permiso VALUES (2,"Modificar Usuarios",1);
INSERT INTO rol_permiso VALUES (3,"Ver Usuarios",1);

INSERT INTO rol_permiso VALUES (4,"Ver Roles",1);
INSERT INTO rol_permiso VALUES (5,"Crear Roles",1);
INSERT INTO rol_permiso VALUES (6,"Modificar Roles",1);


-----------TABLA ROL_ROL----------
INSERT INTO rol_rol VALUES (1, false, "Administrador", "Administra los usuarios del sistema");


----------TABLA ROL_ROL_PERMISOS-----------
INSERT INTO rol_rol_permisos VALUES (1,1,1);
INSERT INTO rol_rol_permisos VALUES (2,1,2);
INSERT INTO rol_rol_permisos VALUES (3,1,3);


----------TABLA USUARIOS_PERMISOS---------
INSERT INTO usuarios_usuario_permisos VALUES (1,1,1);
INSERT INTO usuarios_usuario_permisos VALUES (2,1,2);
INSERT INTO usuarios_usuario_permisos VALUES (3,1,3);
INSERT INTO usuarios_usuario_permisos VALUES (4,1,4);
INSERT INTO usuarios_usuario_permisos VALUES (5,1,5);
INSERT INTO usuarios_usuario_permisos VALUES (6,1,6);

