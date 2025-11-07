import React, {createContext, useContext, useState, useEffect} from 'react';
import {authAPI} from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({children}) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Initialisation - Vérifier si un token existe
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        const userData = localStorage.getItem('user');

        if (token && userData) {
          const parsedUser = JSON.parse(userData);
          setUser(parsedUser);
          setIsAuthenticated(true);

          // Vérifier si le token est encore valide
          try {
            await authAPI.getProfile();
          } catch (error) {
            // Token invalide, déconnecter
            logout();
          }
        }
      } catch (error) {
        console.error('Erreur initialisation auth:', error);
        logout();
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password);
      const {token, user: userData} = response;

      // Stocker les données
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(userData));

      setUser(userData);
      setIsAuthenticated(true);

      return {success: true};
    } catch (error) {
      console.error('Erreur de connexion:', error);
      return {
        success: false,
        error: error.response?.data?.error || 'Erreur de connexion'
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      const {token, user: newUser} = response;

      // Connexion automatique après inscription
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(newUser));

      setUser(newUser);
      setIsAuthenticated(true);

      return {success: true};
    } catch (error) {
      console.error("Erreur d'inscription:", error);
      return {
        success: false,
        error: error.response?.data?.error || "Erreur d'inscription"
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setIsAuthenticated(false);
  };

  const updateUser = (updatedUserData) => {
    const newUser = {...user, ...updatedUserData};
    setUser(newUser);
    localStorage.setItem('user', JSON.stringify(newUser));
  };

  const getToken = () => {
    return localStorage.getItem('token');
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    updateUser,
    getToken
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
