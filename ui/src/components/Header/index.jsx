import React from 'react';
import { connect } from 'react-redux';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import MenuIcon from '@material-ui/icons/Menu';
import AppBar from '@material-ui/core/AppBar';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import InputAdornment from '@material-ui/core/InputAdornment';
import SearchIcon from '@material-ui/icons/Search';
import CloseIcon from '@material-ui/icons/Close';
import AddIcon from '@material-ui/icons/Add';

import requests from '../../lib/requests';

import { setSearchValue as setSearchValueAction } from './actions';
import useStyles from './styles';


function Header({ title, search, addBtn, setSearchValue, handleDrawerToggle }) {
  const classes = useStyles();
  const handleSearch = ({ target: { value } }) => {
    setSearchValue(value);
    search.onSearch(value);
  };
  const clearSearch = () => {
    setSearchValue('');
    search.onSearch(null);
  };

  return (
    <AppBar position="fixed" className={classes.appBar}>
      <Toolbar>
        <IconButton
          onClick={handleDrawerToggle}
          className={classes.menuButton}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap>
          {title}
        </Typography>
        {addBtn.onClick &&
          <Button
            className={classes.addButton}
            startIcon={<AddIcon />}
            onClick={addBtn.onClick}
          >
            {addBtn.text}
          </Button>}
        <div className={classes.grow} />
        {search.onSearch &&
          <TextField
            className={classes.search}
            value={search.value}
            onChange={handleSearch}
            variant="outlined"
            placeholder={search.placeholder}
            InputProps={{
              classes: {
                root: classes.searchInputRoot,
                input: classes.searchInput,
              },
              startAdornment: (
                <InputAdornment>
                  <SearchIcon />
                </InputAdornment>
              ),
              endAdornment: (
                search.value
                  ? (
                    <InputAdornment>
                      <CloseIcon
                        onClick={clearSearch}
                        className={classes.searchClose}
                      />
                    </InputAdornment>
                  )
                  : null
              ),
            }}
          />}
        <Button
          color="primary"
          onClick={
            () => requests.post('/users/logout/').then(
              () => window.location = '/'
            )
          }
        >
          Выйти
        </Button>
      </Toolbar>
    </AppBar>
  );
}

const mapStateToProps = ({ headerReducer }) => ({ ...headerReducer });

const mapDispatchToProps = {
  setSearchValue: setSearchValueAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);
