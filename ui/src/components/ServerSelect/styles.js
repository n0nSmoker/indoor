export default theme => ({
  root: {
    paddingRight: 5,
  },
  adornment: {
    padding: 2,
  },
  popper: {
    zIndex: theme.zIndex.modal,
  },
  paper: {
    ...theme.typography.body1,
    overflow: 'hidden',
    margin: '4px 0',
    '& > ul': {
      maxHeight: '40vh',
      overflow: 'auto',
    },
  },
  optionsList: {
    listStyle: 'none',
    margin: 0,
    padding: '8px 0px',
  },
  option: {
    cursor: 'pointer',
    padding: '6px 16px',
    [theme.breakpoints.up('sm')]: {
      minHeight: 'auto',
    },
    [theme.breakpoints.down('sm')]: {
      lineHeight: 2.3,
    },
    '&:hover': {
      backgroundColor: theme.palette.action.hover,
    },
    '&.selected': {
      backgroundColor: theme.palette.action.selected,
    },
  },
  noResults: {
    color: theme.palette.text.secondary,
    textAlign: 'center',
    padding: '8px 0',
  },
});
