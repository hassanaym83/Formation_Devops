import React from 'react';
import ReactDOM from 'react-dom/client';
import {BrowserRouter} from 'react-router-dom';
import {QueryClient, QueryClientProvider} from 'react-query';
import {ThemeProvider, createTheme} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import {Toaster} from 'react-hot-toast';

import App from './App.jsx';
import {AdminAuthProvider} from './contexts/AdminAuthContext.jsx';
import './index.css';

// Configuration React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000 // 5 minutes
    }
  }
});

// Thème Material-UI pour l'admin
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Bleu pour l'admin
      light: '#42a5f5',
      dark: '#1565c0'
    },
    secondary: {
      main: '#d32f2f'
    },
    background: {
      default: '#f5f5f5'
    }
  },
  typography: {
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600
    }
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8
        }
      }
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          borderRadius: 12
        }
      }
    }
  }
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>
          <AdminAuthProvider>
            <App />
            <Toaster
              position='top-right'
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#333',
                  color: '#fff'
                }
              }}
            />
          </AdminAuthProvider>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
