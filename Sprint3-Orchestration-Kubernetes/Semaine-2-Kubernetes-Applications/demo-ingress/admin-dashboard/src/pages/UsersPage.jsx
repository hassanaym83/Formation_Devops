import React, {useState, useEffect} from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  IconButton,
  Chip,
  TextField,
  InputAdornment,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  CircularProgress,
  Avatar
} from '@mui/material';
import {
  Search,
  Edit,
  Block,
  CheckCircle,
  Person,
  Email,
  Phone,
  LocationOn,
  Refresh
} from '@mui/icons-material';
import {adminAPI, apiUtils} from '../services/api';

const UsersPage = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(20);
  const [total, setTotal] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [selectedUser, setSelectedUser] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    loadUsers();
  }, [page, rowsPerPage, searchTerm, statusFilter]);

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await adminAPI.getUsers(
        page + 1, // API utilise une pagination basée sur 1
        rowsPerPage,
        searchTerm,
        statusFilter
      );

      setUsers(response.users || []);
      setTotal(response.total || 0);
    } catch (err) {
      console.error('Erreur lors du chargement des utilisateurs:', err);
      setError(apiUtils.handleError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
    setPage(0); // Reset à la première page lors d'une recherche
  };

  const handleStatusFilterChange = (event) => {
    setStatusFilter(event.target.value);
    setPage(0);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleUserClick = async (userId) => {
    try {
      const userDetails = await adminAPI.getUserById(userId);
      setSelectedUser(userDetails);
      setDialogOpen(true);
    } catch (err) {
      console.error('Erreur lors du chargement des détails utilisateur:', err);
      setError(apiUtils.handleError(err));
    }
  };

  const handleToggleUserStatus = async (userId) => {
    try {
      await adminAPI.toggleUserStatus(userId);
      loadUsers(); // Recharger la liste
      setDialogOpen(false);
    } catch (err) {
      console.error('Erreur lors du changement de statut:', err);
      setError(apiUtils.handleError(err));
    }
  };

  const getStatusChip = (status) => {
    switch (status) {
      case 'active':
        return <Chip label='Actif' color='success' size='small' />;
      case 'inactive':
        return <Chip label='Inactif' color='default' size='small' />;
      case 'suspended':
        return <Chip label='Suspendu' color='error' size='small' />;
      case 'pending':
        return <Chip label='En attente' color='warning' size='small' />;
      default:
        return <Chip label={status} size='small' />;
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <Container maxWidth='lg' sx={{mt: 4, mb: 4}}>
      {/* En-tête */}
      <Box
        sx={{
          mb: 4,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <Box>
          <Typography variant='h4' gutterBottom>
            Gestion des utilisateurs
          </Typography>
          <Typography variant='body1' color='text.secondary'>
            {total} utilisateur{total > 1 ? 's' : ''} inscrit
            {total > 1 ? 's' : ''}
          </Typography>
        </Box>
        <Button
          variant='outlined'
          startIcon={<Refresh />}
          onClick={loadUsers}
          disabled={loading}
        >
          Actualiser
        </Button>
      </Box>

      {/* Filtres */}
      <Card sx={{mb: 3}}>
        <CardContent>
          <Box
            sx={{
              display: 'flex',
              gap: 2,
              alignItems: 'center',
              flexWrap: 'wrap'
            }}
          >
            <TextField
              placeholder='Rechercher par nom, email...'
              variant='outlined'
              size='small'
              value={searchTerm}
              onChange={handleSearchChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position='start'>
                    <Search />
                  </InputAdornment>
                )
              }}
              sx={{minWidth: 250}}
            />
            <FormControl size='small' sx={{minWidth: 150}}>
              <InputLabel>Statut</InputLabel>
              <Select
                value={statusFilter}
                label='Statut'
                onChange={handleStatusFilterChange}
              >
                <MenuItem value=''>Tous</MenuItem>
                <MenuItem value='active'>Actif</MenuItem>
                <MenuItem value='inactive'>Inactif</MenuItem>
                <MenuItem value='suspended'>Suspendu</MenuItem>
                <MenuItem value='pending'>En attente</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </CardContent>
      </Card>

      {/* Messages d'erreur */}
      {error && (
        <Alert severity='error' sx={{mb: 3}} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* Tableau des utilisateurs */}
      <Card>
        <CardContent sx={{p: 0}}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Utilisateur</TableCell>
                  <TableCell>Contact</TableCell>
                  <TableCell>Statut</TableCell>
                  <TableCell>Inscrit le</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={5} align='center' sx={{py: 4}}>
                      <CircularProgress />
                    </TableCell>
                  </TableRow>
                ) : users.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} align='center' sx={{py: 4}}>
                      Aucun utilisateur trouvé
                    </TableCell>
                  </TableRow>
                ) : (
                  users.map((user) => (
                    <TableRow key={user.id} hover>
                      <TableCell>
                        <Box sx={{display: 'flex', alignItems: 'center'}}>
                          <Avatar sx={{mr: 2, bgcolor: 'primary.main'}}>
                            {user.firstName?.charAt(0) || user.email?.charAt(0)}
                          </Avatar>
                          <Box>
                            <Typography variant='subtitle2'>
                              {user.firstName} {user.lastName}
                            </Typography>
                            <Typography
                              variant='caption'
                              color='text.secondary'
                            >
                              ID: {user.id}
                            </Typography>
                          </Box>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box>
                          <Box
                            sx={{
                              display: 'flex',
                              alignItems: 'center',
                              mb: 0.5
                            }}
                          >
                            <Email
                              fontSize='small'
                              sx={{mr: 1, color: 'text.secondary'}}
                            />
                            <Typography variant='body2'>
                              {user.email}
                            </Typography>
                          </Box>
                          {user.phone && (
                            <Box
                              sx={{
                                display: 'flex',
                                alignItems: 'center',
                                mb: 0.5
                              }}
                            >
                              <Phone
                                fontSize='small'
                                sx={{mr: 1, color: 'text.secondary'}}
                              />
                              <Typography variant='body2'>
                                {user.phone}
                              </Typography>
                            </Box>
                          )}
                          {user.city && (
                            <Box sx={{display: 'flex', alignItems: 'center'}}>
                              <LocationOn
                                fontSize='small'
                                sx={{mr: 1, color: 'text.secondary'}}
                              />
                              <Typography variant='body2'>
                                {user.city}
                              </Typography>
                            </Box>
                          )}
                        </Box>
                      </TableCell>
                      <TableCell>{getStatusChip(user.status)}</TableCell>
                      <TableCell>{formatDate(user.createdAt)}</TableCell>
                      <TableCell>
                        <IconButton
                          size='small'
                          onClick={() => handleUserClick(user.id)}
                          title='Voir les détails'
                        >
                          <Edit />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[10, 20, 50, 100]}
            component='div'
            count={total}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
            labelRowsPerPage='Lignes par page:'
            labelDisplayedRows={({from, to, count}) =>
              `${from}-${to} sur ${count !== -1 ? count : `plus de ${to}`}`
            }
          />
        </CardContent>
      </Card>

      {/* Dialog détails utilisateur */}
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth='sm'
        fullWidth
      >
        <DialogTitle>Détails de l'utilisateur</DialogTitle>
        <DialogContent>
          {selectedUser && (
            <Box sx={{pt: 2}}>
              <Box sx={{display: 'flex', alignItems: 'center', mb: 3}}>
                <Avatar
                  sx={{width: 64, height: 64, mr: 2, bgcolor: 'primary.main'}}
                >
                  <Person sx={{fontSize: 32}} />
                </Avatar>
                <Box>
                  <Typography variant='h6'>
                    {selectedUser.firstName} {selectedUser.lastName}
                  </Typography>
                  <Typography variant='body2' color='text.secondary'>
                    {selectedUser.email}
                  </Typography>
                  {getStatusChip(selectedUser.status)}
                </Box>
              </Box>

              <Typography variant='h6' gutterBottom>
                Informations personnelles
              </Typography>
              <Box sx={{mb: 2}}>
                <Typography variant='body2'>
                  <strong>Téléphone:</strong>{' '}
                  {selectedUser.phone || 'Non renseigné'}
                </Typography>
                <Typography variant='body2'>
                  <strong>Date de naissance:</strong>{' '}
                  {formatDate(selectedUser.dateOfBirth) || 'Non renseignée'}
                </Typography>
                <Typography variant='body2'>
                  <strong>Groupe sanguin:</strong>{' '}
                  {selectedUser.bloodType || 'Non renseigné'}
                </Typography>
                <Typography variant='body2'>
                  <strong>Ville:</strong>{' '}
                  {selectedUser.city || 'Non renseignée'}
                </Typography>
                <Typography variant='body2'>
                  <strong>Inscrit le:</strong>{' '}
                  {formatDate(selectedUser.createdAt)}
                </Typography>
              </Box>

              <Typography variant='h6' gutterBottom>
                Statistiques
              </Typography>
              <Box sx={{mb: 2}}>
                <Typography variant='body2'>
                  <strong>Nombre de dons:</strong>{' '}
                  {selectedUser.donationsCount || 0}
                </Typography>
                <Typography variant='body2'>
                  <strong>Dernier don:</strong>{' '}
                  {formatDate(selectedUser.lastDonation) || 'Jamais'}
                </Typography>
                <Typography variant='body2'>
                  <strong>RDV programmés:</strong>{' '}
                  {selectedUser.appointmentsCount || 0}
                </Typography>
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Fermer</Button>
          {selectedUser && (
            <Button
              variant='contained'
              color={selectedUser.status === 'active' ? 'error' : 'success'}
              startIcon={
                selectedUser.status === 'active' ? <Block /> : <CheckCircle />
              }
              onClick={() => handleToggleUserStatus(selectedUser.id)}
            >
              {selectedUser.status === 'active' ? 'Suspendre' : 'Activer'}
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default UsersPage;
