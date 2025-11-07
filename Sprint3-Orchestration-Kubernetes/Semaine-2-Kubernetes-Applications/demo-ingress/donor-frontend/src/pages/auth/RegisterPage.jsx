import React, {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  InputAdornment,
  IconButton
} from '@mui/material';
// Icons removed
import {useForm} from 'react-hook-form';
import toast from 'react-hot-toast';

import {useAuth} from '../../contexts/AuthContext';

const RegisterPage = () => {
  const {register: registerUser} = useAuth();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    watch,
    formState: {errors}
  } = useForm();

  const password = watch('password');

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');

    try {
      const userData = {
        first_name: data.first_name,
        last_name: data.last_name,
        email: data.email,
        password: data.password,
        phone: data.phone,
        birth_date: data.birth_date,
        address: data.address,
        city: data.city,
        postal_code: data.postal_code,
        blood_type: data.blood_group,
        gender: data.gender
      };

      const result = await registerUser(userData);

      if (result.success) {
        toast.success('Inscription réussie ! Bienvenue !');
        navigate('/');
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError("Erreur inattendue lors de l'inscription");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth='md'>
      <Box sx={{py: 4}}>
        <Paper elevation={3} sx={{p: 4}}>
          <Box sx={{textAlign: 'center', mb: 3}}>
            <Typography
              variant='h4'
              gutterBottom
              sx={{fontWeight: 'bold', color: 'primary.main'}}
            >
              Devenir donneur
            </Typography>
            <Typography variant='body1' color='text.secondary'>
              Rejoignez notre communauté de donneurs de sang
            </Typography>
          </Box>

          {error && (
            <Alert severity='error' sx={{mb: 3}}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit(onSubmit)}>
            {/* Informations personnelles */}
            <Typography
              variant='h6'
              gutterBottom
              sx={{mt: 2, mb: 2, fontWeight: 'bold'}}
            >
              Informations personnelles
            </Typography>

            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label='Prénom'
                  {...register('first_name', {
                    required: 'Le prénom est requis',
                    minLength: {value: 2, message: 'Minimum 2 caractères'}
                  })}
                  error={!!errors.first_name}
                  helperText={errors.first_name?.message}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label='Nom de famille'
                  {...register('last_name', {
                    required: 'Le nom est requis',
                    minLength: {value: 2, message: 'Minimum 2 caractères'}
                  })}
                  error={!!errors.last_name}
                  helperText={errors.last_name?.message}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label='Adresse e-mail'
                  type='email'
                  {...register('email', {
                    required: "L'e-mail est requis",
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: "Format d'e-mail invalide"
                    }
                  })}
                  error={!!errors.email}
                  helperText={errors.email?.message}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label='Téléphone'
                  {...register('phone', {
                    required: 'Le téléphone est requis',
                    pattern: {
                      value: /^[0-9+\-\s()]+$/,
                      message: 'Format de téléphone invalide'
                    }
                  })}
                  error={!!errors.phone}
                  helperText={errors.phone?.message}
                />
              </Grid>

              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  label='Date de naissance'
                  type='date'
                  InputLabelProps={{shrink: true}}
                  {...register('birth_date', {
                    required: 'La date de naissance est requise'
                  })}
                  error={!!errors.birth_date}
                  helperText={errors.birth_date?.message}
                />
              </Grid>

              <Grid item xs={12} sm={4}>
                <FormControl fullWidth error={!!errors.gender}>
                  <InputLabel>Sexe</InputLabel>
                  <Select
                    label='Sexe'
                    {...register('gender', {required: 'Le sexe est requis'})}
                  >
                    <MenuItem value='M'>Homme</MenuItem>
                    <MenuItem value='F'>Femme</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={4}>
                <FormControl fullWidth error={!!errors.blood_group}>
                  <InputLabel>Groupe sanguin</InputLabel>
                  <Select
                    label='Groupe sanguin'
                    {...register('blood_group', {
                      required: 'Le groupe sanguin est requis'
                    })}
                  >
                    <MenuItem value='O+'>O+</MenuItem>
                    <MenuItem value='O-'>O-</MenuItem>
                    <MenuItem value='A+'>A+</MenuItem>
                    <MenuItem value='A-'>A-</MenuItem>
                    <MenuItem value='B+'>B+</MenuItem>
                    <MenuItem value='B-'>B-</MenuItem>
                    <MenuItem value='AB+'>AB+</MenuItem>
                    <MenuItem value='AB-'>AB-</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            {/* Adresse */}
            <Typography
              variant='h6'
              gutterBottom
              sx={{mt: 3, mb: 2, fontWeight: 'bold'}}
            >
              Adresse
            </Typography>

            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label='Adresse complète'
                  {...register('address', {
                    required: "L'adresse est requise"
                  })}
                  error={!!errors.address}
                  helperText={errors.address?.message}
                />
              </Grid>

              <Grid item xs={12} sm={8}>
                <TextField
                  fullWidth
                  label='Ville'
                  {...register('city', {
                    required: 'La ville est requise'
                  })}
                  error={!!errors.city}
                  helperText={errors.city?.message}
                />
              </Grid>

              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  label='Code postal'
                  {...register('postal_code', {
                    required: 'Le code postal est requis',
                    pattern: {
                      value: /^[0-9]{5}$/,
                      message: 'Code postal invalide (5 chiffres)'
                    }
                  })}
                  error={!!errors.postal_code}
                  helperText={errors.postal_code?.message}
                />
              </Grid>
            </Grid>

            {/* Informations médicales */}
            <Typography
              variant='h6'
              gutterBottom
              sx={{mt: 3, mb: 2, fontWeight: 'bold'}}
            >
              Informations médicales
            </Typography>

            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label='Poids (kg)'
                  type='number'
                  {...register('weight_kg', {
                    required: 'Le poids est requis',
                    min: {value: 50, message: 'Poids minimum 50kg pour donner'},
                    max: {value: 200, message: 'Poids maximum 200kg'}
                  })}
                  error={!!errors.weight_kg}
                  helperText={errors.weight_kg?.message}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label='Taille (cm)'
                  type='number'
                  {...register('height_cm', {
                    required: 'La taille est requise',
                    min: {value: 140, message: 'Taille minimum 140cm'},
                    max: {value: 220, message: 'Taille maximum 220cm'}
                  })}
                  error={!!errors.height_cm}
                  helperText={errors.height_cm?.message}
                />
              </Grid>
            </Grid>

            {/* Mot de passe */}
            <Typography
              variant='h6'
              gutterBottom
              sx={{mt: 3, mb: 2, fontWeight: 'bold'}}
            >
              Sécurité
            </Typography>

            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label='Mot de passe'
                  type={showPassword ? 'text' : 'password'}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position='end'>
                        <IconButton
                          onClick={() => setShowPassword(!showPassword)}
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
                      message: 'Minimum 6 caractères'
                    }
                  })}
                  error={!!errors.password}
                  helperText={errors.password?.message}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label='Confirmer le mot de passe'
                  type={showConfirmPassword ? 'text' : 'password'}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position='end'>
                        <IconButton
                          onClick={() =>
                            setShowConfirmPassword(!showConfirmPassword)
                          }
                        >
                          {showConfirmPassword ? '🙈' : '👁️'}
                        </IconButton>
                      </InputAdornment>
                    )
                  }}
                  {...register('confirmPassword', {
                    required: 'Veuillez confirmer le mot de passe',
                    validate: (value) =>
                      value === password ||
                      'Les mots de passe ne correspondent pas'
                  })}
                  error={!!errors.confirmPassword}
                  helperText={errors.confirmPassword?.message}
                />
              </Grid>
            </Grid>

            {/* Acceptation des conditions */}
            <FormControlLabel
              control={
                <Checkbox
                  {...register('acceptTerms', {
                    required: 'Vous devez accepter les conditions'
                  })}
                />
              }
              label="J'accepte les conditions d'utilisation et la politique de confidentialité"
              sx={{mt: 2}}
            />
            {errors.acceptTerms && (
              <Typography variant='caption' color='error'>
                {errors.acceptTerms.message}
              </Typography>
            )}

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
                'Créer mon compte'
              )}
            </Button>
          </form>

          <Box sx={{textAlign: 'center', mt: 2}}>
            <Typography variant='body2' color='text.secondary'>
              Déjà un compte ?{' '}
              <Link
                to='/login'
                style={{
                  color: '#d32f2f',
                  textDecoration: 'none',
                  fontWeight: 'bold'
                }}
              >
                Connectez-vous ici
              </Link>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default RegisterPage;
