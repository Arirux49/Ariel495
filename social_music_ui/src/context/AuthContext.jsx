import React, { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../services/AuthService";

const AuthContext = createContext(null);
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(() => authService.getCurrentUser());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const t = authService.getToken();
    if (t && !user) {
      try {
        const u = JSON.parse(atob(t.split(".")[1]));
        localStorage.setItem("userInfo", JSON.stringify(u));
        setUser(u);
      } catch {}
    }
  }, []); // solo al montar

  const login = async (email, password) => {
    setLoading(true);
    try {
      const data = await authService.login(email, password);
      const u = authService.getCurrentUser();
      setUser(u);
      navigate("/dashboard", { replace: true });
      return data;
    } finally {
      setLoading(false);
    }
  };

  const register = async (name, lastname, email, password) => {
    setLoading(true);
    try {
      return await authService.register(name, lastname, email, password);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    navigate("/login", { replace: true });
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        isAuthenticated: authService.isAuthenticated,
        getToken: authService.getToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
