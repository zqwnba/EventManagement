begin;

-- event
INSERT INTO event (`id`, `name`, `location`, `start_time`, `end_time`, `email`, 'delete_flag') VALUES (0, 'FUJI ROCK FESTIVAL ''20', 'Naeba Ski Resort, Yuzawa-cho, Niigata Pref.', '2020-08-21 10:00:00', '2020-08-23 17:00:00', 'contact@fujirockfestival.com', 0);
INSERT INTO event (`id`, `name`, `location`, `start_time`, `end_time`, `email`, 'delete_flag') VALUES (1, 'FUJI ROCK FESTIVAL ''19', 'Naeba Ski Resort, Yuzawa-cho, Niigata Pref.', '2019-08-21 10:00:00', '2019-08-23 17:00:00', 'contact@fujirockfestival.com', 0);
INSERT INTO event (`id`, `name`, `location`, `start_time`, `end_time`, `email`, 'delete_flag') VALUES (2, 'FUJI ROCK FESTIVAL ''18', 'Naeba Ski Resort, Yuzawa-cho, Niigata Pref.', '2018-08-21 10:00:00', '2018-08-23 17:00:00', 'contact@fujirockfestival.com', 0);
INSERT INTO event (`id`, `name`, `location`, `start_time`, `end_time`, `email`, 'delete_flag') VALUES (3, 'FUJI ROCK FESTIVAL ''17', 'Naeba Ski Resort, Yuzawa-cho, Niigata Pref.', '2017-08-21 10:00:00', '2017-08-23 17:00:00', 'contact@fujirockfestival.com', 0);
INSERT INTO event (`id`, `name`, `location`, `start_time`, `end_time`, `email`, 'delete_flag') VALUES (4, 'FUJI ROCK FESTIVAL ''16', 'Naeba Ski Resort, Yuzawa-cho, Niigata Pref.', '2016-08-21 10:00:00', '2016-08-23 17:00:00', 'contact@fujirockfestival.com', 0);

-- user
INSERT INTO user (`email`, `id`) VALUES ('user1@gmail.com', 0);
INSERT INTO user (`email`, `id`) VALUES ('user2@gmail.com', 1);

-- sign up
INSERT INTO signup (`id`, `user_id`, `event_id`) VALUES (0, 1, 2);

commit;