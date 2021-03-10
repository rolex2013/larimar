INSERT INTO menu_menu (`id`,`name`,`slug`,`base_url`,`description`) VALUES (1,'Главное меню','main_menu','/base.html','Меню после авторизации');
INSERT INTO menu_menu (`id`,`name`,`slug`,`base_url`,`description`) VALUES (2,'Вход и Регистрация','logout_menu','/accounts/logout/','');

INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (1,10,'/main/','Главная',0,1,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (2,40,'/projects/projects_page0/','Проекты',0,1,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (3,70,'/accounts/logout/','Выход',0,1,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (5,60,'/accounts/profile0/','Мой профиль',0,1,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (6,10,'/accounts/login/','Вход',0,2,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (7,20,'/accounts/register/','Регистрация',0,2,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (8,30,'/finance/','Финансы',0,1,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (9,20,'/companies/companies_page/0/companies','Организации',0,1,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (10,5,'/site/vacancies_page/','Вакансии',0,2,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (11,2,'/','Главная',0,2,0);
INSERT INTO menu_menuitem (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (12,50,'/crm/clients_page0/','Клиенты',0,1,1);

INSERT INTO `auth_group` (`id`,`name`) VALUES (1,'Суперадминистраторы');
INSERT INTO `auth_group` (`id`,`name`) VALUES (2,'Администраторы организаций');
INSERT INTO `auth_group` (`id`,`name`) VALUES (3,'Администраторы подсистем');
INSERT INTO `auth_group` (`id`,`name`) VALUES (4,'Менеджеры организаций');
INSERT INTO `auth_group` (`id`,`name`) VALUES (5,'Менеджеры подсистем');
INSERT INTO `auth_group` (`id`,`name`) VALUES (6,'Руководители организаций');
INSERT INTO `auth_group` (`id`,`name`) VALUES (7,'Исполнители');
INSERT INTO `auth_group` (`id`,`name`) VALUES (8,'Гости');
