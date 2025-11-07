import React, {useState} from 'react';
import {Link, useNavigate, useLocation} from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton
} from '@mui/material';
// Icons removed
import {useForm} from 'react-hook-form';
import toast from 'react-hot-toast';

import {useAuth} from '../../contexts/AuthContext';

const LoginPage = () => {
  const {login} = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');

  const from = location.state?.from?.pathname || '/';

  const {
    register,
    handleSubmit,
    formState: {errors}
  } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');

    try {
      const result = await login(data.email, data.password);

      if (result.success) {
        toast.success('Connexion réussie !');
        navigate(from, {replace: true});
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Erreur inattendue lors de la connexion');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth='sm'>
      <Box sx={{py: 4}}>
        <Paper elevation={3} sx={{p: 4}}>
          <Box sx={{textAlign: 'center', mb: 3}}>
            <Typography
              variant='h4'
              gutterBottom
              sx={{fontWeight: 'bold', color: 'primary.main'}}
            >
              Connexion
            </Typography>
            <Typography variant='body1' color='text.secondary'>
              Accédez à votre espace donneur
            </Typography>
          </Box>

          {error && (
            <Alert severity='error' sx={{mb: 3}}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit(onSubmit)}>
            <TextField
              fullWidth
              label='Adresse e-mail'
              type='email'
              margin='normal'
              {...register('email', {
                required: "L'adresse e-mail est requise",
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: "Format d'e-mail invalide"
                }
              })}
              error={!!errors.email}
              helperText={errors.email?.message}
            />

            <TextField
              fullWidth
              label='Mot de passe'
              type={showPassword ? 'text' : 'password'}
              margin='normal'
              InputProps={{
                endAdornment: (
                  <InputAdornment position='end'>
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge='end'
                    >
                      {showPassword ? '🙈' : '👁️'}
                    </IconButton>
                  </InputAdornment>
                )
              }}
              {...register('password', {
                required: 'Le mot de passe est requis',
                minLength: {
                  value: 6,
                  message: 'Le mot de passe doit contenir au moins 6 caractères'
                }
              })}
              error={!!errors.password}
              helperText={errors.password?.message}
            />

            <Button
              type='submit'
              fullWidth
              variant='contained'
              size='large'
              disabled={loading}
              sx={{mt: 3, mb: 2, py: 1.5}}
            >
              {loading ? (
                <CircularProgress size={24} color='inherit' />
              ) : (
                'Se connecter'
              )}
            </Button>
          </form>

          <Box sx={{textAlign: 'center', mt: 2}}>
            <Typography variant='body2' color='text.secondary'>
              Pas encore de compte ?{' '}
              <Link
                to='/register'
                style={{
                  color: '#d32f2f',
                  textDecoration: 'none',
                  fontWeight: 'bold'
                }}
              >
                Inscrivez-vous ici
              </Link>
            </Typography>
          </Box>

          <Box sx={{textAlign: 'center', mt: 2}}>
            <Typography variant='caption' color='text.secondary'>
              Vous pouvez aussi{' '}
              <Link
                to='/campaigns'
                style={{
                  color: '#d32f2f',
                  textDecoration: 'none'
                }}
              >
                consulter les campagnes sans compte
              </Link>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default LoginPage;
