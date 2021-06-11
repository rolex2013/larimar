/*
INSERT INTO `auth_group` (`id`,`name`) VALUES (1,'Суперадминистраторы');
INSERT INTO `auth_group` (`id`,`name`) VALUES (2,'Администраторы организаций');
INSERT INTO `auth_group` (`id`,`name`) VALUES (3,'Администраторы подсистем');
INSERT INTO `auth_group` (`id`,`name`) VALUES (4,'Менеджеры организаций');
INSERT INTO `auth_group` (`id`,`name`) VALUES (5,'Менеджеры подсистем');
INSERT INTO `auth_group` (`id`,`name`) VALUES (6,'Руководители организаций');
INSERT INTO `auth_group` (`id`,`name`) VALUES (7,'Исполнители');
INSERT INTO `auth_group` (`id`,`name`) VALUES (8,'Гости');
INSERT INTO `auth_group` (`id`,`name`) VALUES (9,'Клиенты');

INSERT INTO `menu_menu` (`id`,`name`,`slug`,`base_url`,`description`) VALUES (1,'Главное меню','main_menu','/base.html','Меню после авторизации');
INSERT INTO `menu_menu` (`id`,`name`,`slug`,`base_url`,`description`) VALUES (2,'Вход и Регистрация','logout_menu','/accounts/logout/','');
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (1,10,'/main/','Главная',0,1,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (2,40,'/projects/projects_page0/','Проекты',0,1,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (3,70,'/accounts/logout/','Выход',0,1,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (5,60,'/accounts/profile0/','Мой профиль',0,1,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (6,10,'/accounts/login/','Вход',0,2,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (7,20,'/accounts/register/','Регистрация',0,2,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (8,30,'/finance/','Финансы',0,1,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (9,20,'/companies/companies_page/0/companies','Организации',0,1,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (10,5,'/site/vacancies_page/','Вакансии',0,2,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (11,2,'/','Главная',0,2,0);
INSERT INTO `menu_menuitem` (`id`,`order`,`link_url`,`title`,`anonymous_only`,`menu_id`,`login_required`) VALUES (12,50,'/crm/clients_page0/','Клиенты',0,1,1);

INSERT INTO `main_menu` (`id`,`name`,`slug`,`base_url`,`description`,`is_active`) VALUES (1,'Вход и регистрация','vhod-i-registratsiya','/accounts/logout/','',1);
INSERT INTO `main_menu` (`id`,`name`,`slug`,`base_url`,`description`,`is_active`) VALUES (2,'Главное меню','glavnoe-menu','/base.html','Меню после авторизации',1);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (1,'Главная','/',5,1,1,2,4,0,1,1,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (2,'Вакансии','/site/vacancies_page/',10,1,1,2,1,0,1,1,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (3,'Вход','/accounts/login/',15,1,1,2,2,0,1,1,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (4,'Регистрация','/accounts/register/',20,1,1,2,10,0,1,1,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (5,'Главная','/main/',5,1,1,2,5,0,1,2,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (6,'Организации','/companies/companies_page/0/companies',10,1,1,4,8,0,4,2,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (7,'Финансы','/finance/',15,1,2,3,8,1,4,2,'',6);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (8,'Проекты','/projects/projects_page0/',20,1,1,2,9,0,5,2,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (9,'Клиенты','/crm/clients_page0/',25,1,1,2,6,0,6,2,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (10,'Мой профиль','/accounts/profile0/',30,1,1,2,7,0,3,2,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (11,'Выход','/accounts/logout/',35,1,1,2,3,0,1,2,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (12,'Документы','/docs/',17,1,1,6,6,0,7,2,'',NULL);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (13,'Документооборот','/docs/docs_page0/',18,1,2,3,6,1,7,2,'',12);
INSERT INTO `main_menuitem` (`id`,`title`,`link_url`,`sort`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`component_id`,`menu_id`,`description`,`parent_id`) VALUES (14,'Файлы','/docs/file_list/',19,1,4,5,6,1,7,2,'',12);

INSERT INTO `main_dict_protocoltype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'e-mail',1,'e-mail',1);
INSERT INTO `main_dict_protocoltype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'sms',5,'sms',1);
INSERT INTO `main_dict_protocoltype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'local',10,'local',1);
INSERT INTO `main_component` (`id`,`name`,`is_active`,`level`,`lft`,`rght`,`tree_id`,`menu`,`description`,`parent_id`) VALUES (1,'Main',1,0,1,2,2,'Главная','Компонент общих данных и настроек',NULL);
INSERT INTO `main_component` (`id`,`name`,`is_active`,`level`,`lft`,`rght`,`tree_id`,`menu`,`description`,`parent_id`) VALUES (2,'Админка',1,0,1,2,3,'Админка','Компонент администрирования',NULL);
INSERT INTO `main_component` (`id`,`name`,`is_active`,`level`,`lft`,`rght`,`tree_id`,`menu`,`description`,`parent_id`) VALUES (3,'Пользователи',1,0,1,2,6,'Пользователи','Аккаунты, права, роли',NULL);
INSERT INTO `main_component` (`id`,`name`,`is_active`,`level`,`lft`,`rght`,`tree_id`,`menu`,`description`,`parent_id`) VALUES (4,'Организации',1,0,1,2,5,'Организации','Оргструктура и связи с пользователями',NULL);
INSERT INTO `main_component` (`id`,`name`,`is_active`,`level`,`lft`,`rght`,`tree_id`,`menu`,`description`,`parent_id`) VALUES (5,'Проекты и Задачи',1,0,1,2,7,'Проекты','Проекты и трекер задач',NULL);
INSERT INTO `main_component` (`id`,`name`,`is_active`,`level`,`lft`,`rght`,`tree_id`,`menu`,`description`,`parent_id`) VALUES (6,'CRM',1,0,1,2,1,'Клиенты','Работа с клиентами',NULL);
INSERT INTO `main_component` (`id`,`name`,`is_active`,`level`,`lft`,`rght`,`tree_id`,`menu`,`description`,`parent_id`) VALUES (7,'Документооборот',1,0,1,2,4,'Документооборот','Работа с документами и файлами',NULL);
INSERT INTO `main_component` (`id`,`name`,`is_active`,`level`,`lft`,`rght`,`tree_id`,`menu`,`description`,`parent_id`) VALUES (8,'Склад',1,0,1,2,8,'Склад','Перемещение товаров',NULL);
INSERT INTO `main_meta_param` (`id`,`name`,`datecreate`,`is_service`,`is_active`) VALUES (1,'Сервис (тестовый)','2021-03-11 13:00:00.239817',1,1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (1,'cont','Контент','content',1,'Content',1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (2,'org','Организация','company',5,'Company',1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (3,'prj','Проект','project',10,'Project',1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (4,'tsk','Задача','task',15,'Task',1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (5,'cmnt','Комментарий','taskcomments',20,'Comment',1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (7,'clnt','Клиент','client',1,'Client',1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (8,'evnt','Событие','event',25,'Event',1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (9,'doc','Документ','Doc',30,'Document',1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (10,'doctsk','Задача Документа','DocTask',35,'Task of Document',1);
INSERT INTO `main_meta_objecttype` (`id`,`shortname`,`name`,`tablename`,`sort`,`name_lang`,`is_active`) VALUES (11,'doctskcmnt','Комментарий к Задаче Документа','DocTaskComment',40,'Comment',1);
INSERT INTO `crm_dict_clienttaskstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (1,'В разработке',5,'Planing',0,1);
INSERT INTO `crm_dict_clienttaskstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (2,'В работе',10,'Working',0,1);
INSERT INTO `crm_dict_clienttaskstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (3,'Приостановлена',15,'In pause',0,1);
INSERT INTO `crm_dict_clienttaskstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (4,'Решена',20,'Completed',1,1);
INSERT INTO `crm_dict_clienttaskstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (5,'Снята',25,'Canceled',1,1);
INSERT INTO `crm_dict_clienttaskstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (6,'Отклонена',30,'Refused',0,1);
INSERT INTO `crm_dict_clienteventstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (1,'Ожидаемое',5,'',0,1);
INSERT INTO `crm_dict_clienteventstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (2,'Перенесено',10,'',0,1);
INSERT INTO `crm_dict_clienteventstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (3,'Состоялось',15,'',0,1);
INSERT INTO `crm_dict_clienteventstatus` (`id`,`name`,`sort`,`name_lang`,`is_close`,`is_active`) VALUES (4,'Отменено',20,'Canceled',0,1);
INSERT INTO `crm_dict_clienteventtype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Звонок исходящий',10,'',1);
INSERT INTO `crm_dict_clienteventtype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Звонок входящий',15,'',1);
INSERT INTO `crm_dict_clienteventtype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'Встреча онлайн',20,'',1);
INSERT INTO `crm_dict_clienteventtype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (4,'Встреча офлайн',25,NULL,1);
INSERT INTO `crm_client` (`id`,`is_notify`,`firstname`,`middlename`,`lastname`,`email`,`phone`,`description`,`datecreate`,`dateclose`,`is_active`,`author_id`,`company_id`,`manager_id`,`protocoltype_id`,`status_id`,`type_id`,`user_id`,`cost`,`currency_id`,`percentage`,`initiator_id`) VALUES (1,0,'Алексей','Борисович','Квазаров','quasar.a63@gmail.com','+7(916)5555555','<p>Это первый тестовый клиент</p>','2021-01-12 16:28:21.239817',NULL,1,3,8,5,NULL,1,1,NULL,0,1,0,2);
INSERT INTO `crm_client` (`id`,`is_notify`,`firstname`,`middlename`,`lastname`,`email`,`phone`,`description`,`datecreate`,`dateclose`,`is_active`,`author_id`,`company_id`,`manager_id`,`protocoltype_id`,`status_id`,`type_id`,`user_id`,`cost`,`currency_id`,`percentage`,`initiator_id`) VALUES (2,1,'Алексей','Борисович','Квазар','quasar.a63@gmail.com','+7(916)5555555','<p>Это второй тестовый клиент!</p>','2021-01-12 16:34:40.183503',NULL,1,3,8,5,NULL,2,1,NULL,0,1,0,1);
INSERT INTO `crm_dict_clientinitiator` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Клиент',5,'Client',1);
INSERT INTO `crm_dict_clientinitiator` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Организация',10,'Organization',1);
INSERT INTO `crm_dict_clientinitiator` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'Другое',15,'Other',1);
INSERT INTO `crm_dict_clientstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`,`is_close`) VALUES (1,'Новый',5,NULL,1,NULL,0);
INSERT INTO `crm_dict_clientstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`,`is_close`) VALUES (2,'Принимает решение',10,NULL,1,NULL,0);
INSERT INTO `crm_dict_clientstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`,`is_close`) VALUES (3,'Заключил договор',15,NULL,1,NULL,0);
INSERT INTO `crm_dict_clientstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`,`is_close`) VALUES (4,'Клиент',20,NULL,1,NULL,0);
INSERT INTO `crm_dict_clientstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`,`is_close`) VALUES (5,'Неопределённый статус',300,NULL,1,NULL,0);
INSERT INTO `crm_dict_clientstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`,`is_close`) VALUES (6,'Ушедший',35,NULL,1,NULL,1);
INSERT INTO `crm_dict_clientstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`,`is_close`) VALUES (7,'Отказался',40,NULL,1,'',1);
INSERT INTO `crm_dict_clienttasktype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Поручение',NULL,NULL,1);
INSERT INTO `crm_dict_clienttasktype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Простая',NULL,NULL,1);
INSERT INTO `crm_dict_clienttasktype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'Сложная',NULL,NULL,1);
INSERT INTO `crm_dict_clienttaskstructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Основная задача',5,'Main Task',1);
INSERT INTO `crm_dict_clienttaskstructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Подзадача',10,'SubTask',1);
INSERT INTO `crm_dict_clienttype` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`) VALUES (1,'Клиент',5,'Client',1,NULL);
INSERT INTO `crm_dict_clienttype` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`) VALUES (2,'Конкурент',10,NULL,1,NULL);
INSERT INTO `crm_dict_clienttype` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`) VALUES (3,'Контактное лицо',15,NULL,1,NULL);
INSERT INTO `crm_dict_clienttype` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`) VALUES (4,'Подрядчик',20,NULL,1,NULL);
INSERT INTO `crm_dict_clienttype` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`) VALUES (5,'Партнёр',25,NULL,1,NULL);
INSERT INTO `crm_dict_clienttype` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`) VALUES (6,'Поставщик',30,NULL,1,NULL);
INSERT INTO `crm_dict_clienttype` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`) VALUES (7,'Наша компания',35,NULL,1,NULL);
INSERT INTO `crm_dict_clienttype` (`id`,`name`,`sort`,`name_lang`,`is_active`,`description`) VALUES (8,'Сотрудник',40,NULL,1,NULL);

INSERT INTO docs_dict_docstatus (id, name, description, sort, name_lang, is_public, is_active) VALUES (1, 'В разработке', null, 10, null, 0, 1);
*/
INSERT INTO docs_dict_docstatus (id, name, description, sort, name_lang, is_public, is_active) VALUES (2, 'На согласовании', null, 15, null, 0, 1);
INSERT INTO docs_dict_docstatus (id, name, description, sort, name_lang, is_public, is_active) VALUES (3, 'Опубликован', null, 20, null, 1, 1);
/*
INSERT INTO docs_dict_doctaskstatus (id, name, description, sort, name_lang, is_close, is_active) VALUES (1, 'В очереди', '', 10, null, 0, 1);
INSERT INTO docs_dict_doctaskstatus (id, name, description, sort, name_lang, is_close, is_active) VALUES (2, 'В работе', '', 20, null, 0, 1);
INSERT INTO docs_dict_doctaskstatus (id, name, description, sort, name_lang, is_close, is_active) VALUES (3, 'Возврат', '', 30, null, 1, 1);
INSERT INTO docs_dict_doctaskstatus (id, name, description, sort, name_lang, is_close, is_active) VALUES (4, 'Готово', '', 40, null, 1, 1);
INSERT INTO docs_dict_doctaskstatus (id, name, description, sort, name_lang, is_close, is_active) VALUES (5, 'Отказ', '', 50, null, 1, 1);
INSERT INTO docs_dict_doctasktype (id, name, description, sort, name_lang, is_active) VALUES (1, 'На подпись', '', 10, null, 1);
INSERT INTO docs_dict_doctasktype (id, name, description, sort, name_lang, is_active) VALUES (2, 'На согласование', '', 20, null, 1);
INSERT INTO docs_dict_doctasktype (id, name, description, sort, name_lang, is_active) VALUES (3, 'Для ознакомления', '', 30, null, 1);
INSERT INTO docs_dict_doctasktype (id, name, description, sort, name_lang, is_active) VALUES (4, 'Для рецензирования', '', 40, null, 1);
INSERT INTO docs_dict_doctype (id, name, description, sort, name_lang, is_active) VALUES (1, 'Проектный', 'Проектная документация', 10, null, 1);
INSERT INTO docs_dict_doctype (id, name, description, sort, name_lang, is_active) VALUES (2, 'Финансовый', '', 20, null, 1);
INSERT INTO docs_dict_doctype (id, name, description, sort, name_lang, is_active) VALUES (3, 'Управленческий', '', 30, null, 1);

INSERT INTO `projects_dict_projecttype` (`id`,`name`,`sort`,`is_active`,`name_lang`) VALUES (1,'Срочный',1,1,'Immediate');
INSERT INTO `projects_dict_projecttype` (`id`,`name`,`sort`,`is_active`,`name_lang`) VALUES (2,'Обычный',2,1,'Normal');
INSERT INTO `projects_dict_projecttype` (`id`,`name`,`sort`,`is_active`,`name_lang`) VALUES (3,'Простой',3,1,'Simple');
INSERT INTO `projects_dict_projectstructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Проект',1,'Project',1);
INSERT INTO `projects_dict_projectstructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Подпроект',1,'subproject',1);
INSERT INTO `projects_dict_projectstructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'Этап',1,'Stage',1);
INSERT INTO `projects_dict_projectstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (1,'В разработке',1,'Planing',1,0);
INSERT INTO `projects_dict_projectstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (2,'В работе',2,'Working',1,0);
INSERT INTO `projects_dict_projectstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (3,'Приостановлен',3,'In pause',1,0);
INSERT INTO `projects_dict_projectstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (4,'Выполнен',4,'Completed',1,1);
INSERT INTO `projects_dict_projectstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (5,'Отменён',5,'Canceled',1,1);
INSERT INTO `projects_dict_tasktype` (`id`,`name`,`sort`,`is_active`,`name_lang`) VALUES (1,'Поручение',1,1,'Instruction');
INSERT INTO `projects_dict_tasktype` (`id`,`name`,`sort`,`is_active`,`name_lang`) VALUES (2,'Простая',2,1,'Simple');
INSERT INTO `projects_dict_tasktype` (`id`,`name`,`sort`,`is_active`,`name_lang`) VALUES (3,'Сложная',3,1,'Difficult');
INSERT INTO `projects_dict_taskstructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Основная задача',1,'Main Task',1);
INSERT INTO `projects_dict_taskstructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Подзадача',1,'Subtask',1);
INSERT INTO `projects_dict_taskstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (1,'В разработке',1,'Planing',1,0);
INSERT INTO `projects_dict_taskstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (2,'В работе',2,'Working',1,0);
INSERT INTO `projects_dict_taskstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (3,'Приостановлена',3,'In pause',1,0);
INSERT INTO `projects_dict_taskstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (4,'Решена',4,'Completed',1,1);
INSERT INTO `projects_dict_taskstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (5,'Снята',5,'Canceled',1,1);
INSERT INTO `projects_dict_taskstatus` (`id`,`name`,`sort`,`name_lang`,`is_active`,`is_close`) VALUES (6,'Отклонена',6,'Refused',1,0);

INSERT INTO `companies_dict_companytype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Поставщик',5,'Provider',1);
INSERT INTO `companies_dict_companytype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Покупатель',10,'Buyer',1);
INSERT INTO `companies_dict_companytype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'Партнёр',15,'Partner',1);
INSERT INTO `companies_dict_companytype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (4,'Подрядчик',20,'Partner',1);
INSERT INTO `companies_dict_companytype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (5,'Тестовая Компания',25,'Test',1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Головная организация',1,'Main Company',1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Холдинг',1,NULL,1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'Группа компаний',1,NULL,1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (4,'Филиал',1,NULL,1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (5,'Обособленное подразделение',1,NULL,1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (6,'Представительство',1,NULL,1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (7,'Отделение',1,NULL,1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (8,'Отдел',1,NULL,1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (9,'Сектор',1,NULL,1);
INSERT INTO `companies_dict_companystructuretype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (10,'Группа',1,NULL,1);
INSERT INTO `companies_dict_contenttype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Новость',1,'News',1);
INSERT INTO `companies_dict_contenttype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Объявление',5,'Announcement',1);
INSERT INTO `companies_dict_contenttype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'Блог',10,'Blog',1);
INSERT INTO `companies_dict_contenttype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (4,'Заметка',15,'Note',1);
INSERT INTO `companies_dict_contentplace` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Внешний сайт',1,'Site content',1);
INSERT INTO `companies_dict_contentplace` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Контент организации',5,'Company content',1);
INSERT INTO `companies_dict_contentplace` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'Для профиля',10,'Profile content',1);
INSERT INTO `companies_dict_contentplace` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (4,'Личный контент',15,'Private content',1);
INSERT INTO `companies_dict_positiontype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (1,'Руководитель высшего звена',1,NULL,1);
INSERT INTO `companies_dict_positiontype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (2,'Руководитель среднего звена',5,NULL,1);
INSERT INTO `companies_dict_positiontype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (3,'Руководитель низшего звена',10,NULL,1);
INSERT INTO `companies_dict_positiontype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (4,'Специалист',15,NULL,1);
INSERT INTO `companies_dict_positiontype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (5,'Менеджер',20,NULL,1);
INSERT INTO `companies_dict_positiontype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (6,'Инженер',12,NULL,1);
INSERT INTO `companies_dict_positiontype` (`id`,`name`,`sort`,`name_lang`,`is_active`) VALUES (7,'Рабочий',30,NULL,1);

INSERT INTO `finance_dict_currency` (`id`,`code_char`,`code_num`,`name`,`sort`,`name_lang`,`is_active`,`symbol`,`shortname`) VALUES (1,'RUB','643','Российский рубль',1,'Russian ruble',1,'₽','руб.');
INSERT INTO `finance_dict_currency` (`id`,`code_char`,`code_num`,`name`,`sort`,`name_lang`,`is_active`,`symbol`,`shortname`) VALUES (2,'USD','840','Доллар США',3,'US Dollar',1,'$','$');
INSERT INTO `finance_dict_currency` (`id`,`code_char`,`code_num`,`name`,`sort`,`name_lang`,`is_active`,`symbol`,`shortname`) VALUES (3,'EUR','948','Евро',5,'Euro',1,'€','€');


INSERT INTO `companies_company` (`id`,`name`,`description`,`datecreate`,`is_active`,`lft`,`rght`,`tree_id`,`level`,`author_id`,`structure_type_id`,`type_id`,`currency_id`,`parent_id`) VALUES (1,'Larimar IT Group','<p><em><strong><img alt=`` src=`/media/uploads/2020/02/29/larimar_2.png` />&nbsp;Группа компаний Larimar IT Group</strong></em></p>','2020-01-01 00:00:01.490279',1,1,30,1,0,1,1,1,1,NULL);
*/

