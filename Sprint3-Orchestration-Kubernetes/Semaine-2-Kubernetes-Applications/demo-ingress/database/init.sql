-- Base de données pour le système de gestion des dons de sang
-- Création et initialisation des tables

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS dondesang CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dondesang;

-- Table des utilisateurs (donneurs)
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    birth_date DATE NOT NULL,
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    gender ENUM('M', 'F', 'Other'),
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(20),
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_blood_type (blood_type),
    INDEX idx_city (city),
    INDEX idx_status (status)
);

-- Table des profils médicaux
CREATE TABLE IF NOT EXISTS medical_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    weight DECIMAL(5,2), -- en kg
    height INT, -- en cm
    medical_conditions TEXT,
    medications TEXT,
    allergies TEXT,
    eligible_to_donate BOOLEAN DEFAULT TRUE,
    last_donation_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_eligible (eligible_to_donate),
    INDEX idx_last_donation (last_donation_date)
);

-- Table des campagnes de don
CREATE TABLE IF NOT EXISTS campaigns (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    location_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    max_donors_per_day INT DEFAULT 50,
    contact_phone VARCHAR(20),
    contact_email VARCHAR(255),
    urgent BOOLEAN DEFAULT FALSE,
    status ENUM('draft', 'active', 'completed', 'cancelled') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_city (city),
    INDEX idx_dates (start_date, end_date),
    INDEX idx_status (status),
    INDEX idx_urgent (urgent),
    INDEX idx_location (latitude, longitude)
);

-- Table des créneaux de rendez-vous
CREATE TABLE IF NOT EXISTS appointment_slots (
    id INT PRIMARY KEY AUTO_INCREMENT,
    campaign_id INT NOT NULL,
    slot_date DATE NOT NULL,
    slot_time TIME NOT NULL,
    max_appointments INT DEFAULT 5,
    current_appointments INT DEFAULT 0,
    available BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    UNIQUE KEY unique_slot (campaign_id, slot_date, slot_time),
    INDEX idx_campaign_date (campaign_id, slot_date),
    INDEX idx_available (available)
);

-- Table des rendez-vous
CREATE TABLE IF NOT EXISTS appointments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    campaign_id INT NOT NULL,
    slot_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('scheduled', 'confirmed', 'completed', 'cancelled', 'no_show') DEFAULT 'scheduled',
    confirmation_code VARCHAR(10),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    FOREIGN KEY (slot_id) REFERENCES appointment_slots(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_campaign (campaign_id),
    INDEX idx_date (appointment_date),
    INDEX idx_status (status),
    INDEX idx_confirmation (confirmation_code)
);

-- Table de l'historique des dons
CREATE TABLE IF NOT EXISTS donation_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    appointment_id INT,
    donation_date DATE NOT NULL,
    blood_type VARCHAR(5),
    volume_ml INT DEFAULT 450,
    medical_notes TEXT,
    staff_id VARCHAR(100),
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_date (donation_date),
    INDEX idx_blood_type (blood_type)
);

-- Table des administrateurs
CREATE TABLE IF NOT EXISTS admin_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    role ENUM('admin', 'super_admin', 'moderator') DEFAULT 'admin',
    permissions JSON,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_is_active (is_active),
    INDEX idx_role (role)
);

-- Table des logs d'audit
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT,
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(50), -- 'user', 'campaign', 'appointment', etc.
    target_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (admin_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    INDEX idx_admin (admin_id),
    INDEX idx_action (action),
    INDEX idx_target (target_type, target_id),
    INDEX idx_date (created_at)
);

-- Insertion des données de test

-- Administrateurs par défaut 
-- admin / admin123 et superadmin / superadmin123
INSERT INTO admin_users (username, password_hash, first_name, last_name, email, role, permissions) VALUES 
('admin', '$2a$10$cM1yubUl4yxIdhQ9GbhGE.VzOQPXA5E0.yeLL/k1qKBXcpqhW/Psu', 'Admin', 'Principal', 'admin@blooddonation.com', 'admin', '["manage_users", "manage_campaigns"]'),
('superadmin', '$2a$10$EcAJYOBGNlSzMp43RRjmjuO6qy5v.8JKache8LZWRhvcd0I40lbZq', 'Super', 'Administrateur', 'superadmin@blooddonation.com', 'super_admin', '["manage_users", "manage_campaigns", "manage_admins", "view_audit", "system_config"]')
ON DUPLICATE KEY UPDATE username = VALUES(username);

-- Utilisateurs de test (password: password123)
INSERT INTO users (email, password_hash, first_name, last_name, phone, birth_date, blood_type, gender, address, city, postal_code) VALUES 
('john.doe@email.com', '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'John', 'Doe', '0123456789', '1990-05-15', 'O+', 'M', '123 Rue de la République', 'Paris', '75001'),
('marie.martin@email.com', '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Marie', 'Martin', '0987654321', '1985-08-22', 'A+', 'F', '456 Avenue de la Liberté', 'Lyon', '69001'),
('pierre.durand@email.com', '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Pierre', 'Durand', '0147258369', '1992-12-03', 'B-', 'M', '789 Boulevard Saint-Germain', 'Marseille', '13001')
ON DUPLICATE KEY UPDATE email = VALUES(email);

-- Profils médicaux pour les utilisateurs de test
INSERT INTO medical_profiles (user_id, weight, height, eligible_to_donate) VALUES 
((SELECT id FROM users WHERE email = 'john.doe@email.com'), 75.5, 180, TRUE),
((SELECT id FROM users WHERE email = 'marie.martin@email.com'), 62.0, 165, TRUE),
((SELECT id FROM users WHERE email = 'pierre.durand@email.com'), 80.2, 175, TRUE)
ON DUPLICATE KEY UPDATE user_id = VALUES(user_id);

-- Campagnes de test
INSERT INTO campaigns (name, description, location_name, address, city, postal_code, latitude, longitude, start_date, end_date, start_time, end_time, contact_phone, contact_email) VALUES 
('Don de Sang Urgence - Hôpital Central', 'Collecte de sang urgente pour les services de chirurgie cardiaque', 'Hôpital Central de Paris', '1 Place de l\'Hôpital', 'Paris', '75004', 48.8566, 2.3522, '2024-12-01', '2024-12-03', '08:00:00', '18:00:00', '01.42.34.56.78', 'urgence@hopital-central.fr'),
('Collecte Mensuelle - Mairie du 15ème', 'Collecte mensuelle de don du sang organisée par la mairie', 'Mairie du 15ème arrondissement', '31 Rue Péclet', 'Paris', '75015', 48.8387, 2.2827, '2024-12-10', '2024-12-10', '09:00:00', '17:00:00', '01.53.68.15.15', 'sante@mairie15.paris.fr'),
('Don de Noël - Centre Commercial', 'Grande collecte de Noël pour les fêtes', 'Centre Commercial Vélizy', 'Avenue de l\'Europe', 'Vélizy-Villacoublay', '78140', 48.7804, 2.2186, '2024-12-15', '2024-12-20', '10:00:00', '20:00:00', '01.39.46.12.34', 'noel@velizy.fr')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Créneaux de rendez-vous pour les campagnes
INSERT INTO appointment_slots (campaign_id, slot_date, slot_time, max_appointments) VALUES 
-- Campagne 1
(1, '2024-12-01', '08:00:00', 5),
(1, '2024-12-01', '10:00:00', 5),
(1, '2024-12-01', '14:00:00', 5),
(1, '2024-12-01', '16:00:00', 5),
(1, '2024-12-02', '08:00:00', 5),
(1, '2024-12-02', '10:00:00', 5),
(1, '2024-12-02', '14:00:00', 5),
(1, '2024-12-02', '16:00:00', 5),
-- Campagne 2
(2, '2024-12-10', '09:00:00', 8),
(2, '2024-12-10', '11:00:00', 8),
(2, '2024-12-10', '14:00:00', 8),
(2, '2024-12-10', '16:00:00', 8),
-- Campagne 3
(3, '2024-12-15', '10:00:00', 10),
(3, '2024-12-15', '14:00:00', 10),
(3, '2024-12-16', '10:00:00', 10),
(3, '2024-12-16', '14:00:00', 10),
(3, '2024-12-17', '10:00:00', 10),
(3, '2024-12-17', '14:00:00', 10)
ON DUPLICATE KEY UPDATE campaign_id = VALUES(campaign_id);

COMMIT;