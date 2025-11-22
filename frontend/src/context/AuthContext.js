import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      // Verify token and get user info
      axios.get('/api/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(response => {
        if (response.data.success) {
          setUser(response.data.user);
        }
      })
      .catch(() => {
        // Invalid token
        localStorage.removeItem('token');
        setToken(null);
      })
      .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [token]);

  const register = async (username, email, password) => {
    const response = await axios.post('/api/auth/register', {
      username,
      email,
      password
    });
    
    if (response.data.success) {
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      setToken(token);
      setUser(user);
      return { success: true };
    }
    return { success: false };
  };

  const login = async (username, password) => {
    try {
      const response = await axios.post('/api/auth/login', {
        username,
        password
      });
      
      if (response.data.success) {
        const { token, user } = response.data;
        localStorage.setItem('token', token);
        setToken(token);
        setUser(user);
        return { success: true };
      }
      return { success: false, error: 'Login failed' };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const logout = async () => {
    if (token) {
      try {
        await axios.post('/api/auth/logout', {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
      } catch (error) {
        console.error('Logout error:', error);
      }
    }
    
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const addFavorite = async (placeData) => {
    if (!token) return { success: false, error: 'Not authenticated' };
    
    try {
      const response = await axios.post('/api/auth/favorites', 
        { place_data: placeData },
        { headers: { Authorization: `Bearer ${token}` }}
      );
      return { success: response.data.success };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to add favorite' };
    }
  };

  const removeFavorite = async (placeId) => {
    if (!token) return { success: false };
    
    try {
      await axios.delete(`/api/auth/favorites/${placeId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      return { success: true };
    } catch (error) {
      return { success: false };
    }
  };

  const getFavorites = async () => {
    if (!token) return [];
    
    try {
      const response = await axios.get('/api/auth/favorites', {
        headers: { Authorization: `Bearer ${token}` }
      });
      return response.data.favorites;
    } catch (error) {
      return [];
    }
  };

  const checkFavorite = async (placeId) => {
    if (!token) return false;
    
    try {
      const response = await axios.get(`/api/auth/favorites/check/${placeId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      return response.data.is_favorite;
    } catch (error) {
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      token,
      loading,
      register,
      login,
      logout,
      addFavorite,
      removeFavorite,
      getFavorites,
      checkFavorite,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
