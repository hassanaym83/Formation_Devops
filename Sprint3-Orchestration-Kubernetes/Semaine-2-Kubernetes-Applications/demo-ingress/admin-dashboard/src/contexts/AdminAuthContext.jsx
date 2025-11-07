import React, {createContext, useContext, useState, useEffect} from 'react';
import {adminAPI} from '../services/api';

const AdminAuthContext = createContext();

export const useAdminAuth = () => {
  const context = useContext(AdminAuthContext);
  if (!context) {
    throw new Error('useAdminAuth must be used within an AdminAuthProvider');
  }
  return context;
};

export const AdminAuthProvider = ({children}) => {
  const [admin, setAdmin] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Initialisation - Vérifier si un token admin existe
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('adminToken');
        const adminData = localStorage.getItem('adminUser');

        if (token && adminData) {
          const parsedAdmin = JSON.parse(adminData);
          setAdmin(parsedAdmin);
          setIsAuthenticated(true);

          // Note: Ici on pourrait vérifier si le token est encore valide
          // en appelant une route de vérification admin
        }
      } catch (error) {
        console.error('Erreur initialisation auth admin:', error);
        logout();
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (username, password) => {
    try {
      const response = await adminAPI.login(username, password);
      const {token, admin: adminData} = response;

      // Stocker les données admin
      localStorage.setItem('adminToken', token);
      localStorage.setItem('adminUser', JSON.stringify(adminData));

      setAdmin(adminData);
      setIsAuthenticated(true);

      return {success: true};
    } catch (error) {
      console.error('Erreur de connexion admin:', error);
      return {
        success: false,
        error: error.response?.data?.error || 'Erreur de connexion'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminUser');
    setAdmin(null);
    setIsAuthenticated(false);
  };

  const updateAdmin = (updatedAdminData) => {
    const newAdmin = {...admin, ...updatedAdminData};
    setAdmin(newAdmin);
    localStorage.setItem('adminUser', JSON.stringify(newAdmin));
  };

  const getToken = () => {
    return localStorage.getItem('adminToken');
  };

  const hasPermission = (permission) => {
    if (!admin) return false;
    if (admin.role === 'super_admin') return true;

    const permissions = admin.permissions || [];
    return permissions.includes(permission);
  };

  const value = {
    admin,
    isAuthenticated,
    loading,
    login,
    logout,
    updateAdmin,
    getToken,
    hasPermission
  };

  return (
    <AdminAuthContext.Provider value={value}>
      {children}
    </AdminAuthContext.Provider>
  );
};
