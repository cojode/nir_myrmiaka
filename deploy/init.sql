-- Insert static data into the users_group table
INSERT INTO users_group (id, group_name) VALUES
(1, 'test_group_1'),
(2, 'test_group_2'),
(3, 'test_group_2');

INSERT INTO base_researchwork (id, name, description) VALUES
(1, 'Research on AI', 'A comprehensive study on artificial intelligence.'),
(2, 'Climate Change', 'Analyzing the impact of climate change on ecosystems.'),
(3, 'Quantum Computing', 'Exploring the potential of quantum computing.');

INSERT INTO base_topic (id, name, research_work_id) VALUES
(1, 'Machine Learning', 1),
(2, 'Natural Language Processing', 1),
(3, 'Renewable Energy', 2),
(4, 'Carbon Footprint', 2),
(5, 'Qubits', 3),
(6, 'Quantum Algorithms', 3);

INSERT INTO base_submission (id, title, research_work_id) VALUES
(1, 'AI in Healthcare', 1),
(2, 'AI in Finance', 1),
(3, 'Global Warming Trends', 2),
(4, 'Impact on Polar Ice Caps', 2),
(5, 'Quantum Supremacy', 3),
(6, 'Quantum Cryptography', 3);