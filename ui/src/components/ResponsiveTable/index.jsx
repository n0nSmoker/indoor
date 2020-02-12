import React from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';


const useStyles = makeStyles({
  paper: {
    borderRadius: 5,
  },
  tableContainer: {
    backgroundColor: 'white',
    borderTopLeftRadius: 5,
    borderTopRightRadius: 5,
    maxHeight: 'calc(100vh - 220px)',  // TODO: fix it, make dynamic
  },
  headCell: {
    backgroundColor: 'white',
    fontWeight: 'bold',
  },
  serial: {
    width: 100,
  },
  actions: {
    width: 200,
  },
  actionBtn: {
    display: 'block',
    fontWeight: 'bold',
  },
});

// TODO: make responsive
export default function ResponsiveTable({
  items,
  columns,
  actions,
  page,
  onPageChange,
  limit,
  onLimitChange,
  total,
}) {
  const classes = useStyles();
  return (
    <Paper className={classes.paper}>
      <TableContainer className={classes.tableContainer}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell className={cn(classes.serial, classes.headCell)}>№ п/п</TableCell>
              {columns.map(column => (
                <TableCell key={column.key} className={classes.headCell}>
                  {column.title}
                </TableCell>
              ))}
              {actions && actions.length &&
                <TableCell className={classes.headCell}>
                  Действия
                </TableCell>}
            </TableRow>
          </TableHead>
          <TableBody>
            {items.map((row, index) => {
              return (
                <TableRow hover key={row.id}>
                  <TableCell className={classes.serial}>{index + 1}</TableCell>
                  {columns.map(column => {
                    return (
                      <TableCell key={column.key}>
                        {column.getValue ? column.getValue(row) : row[column.key]}
                      </TableCell>
                    );
                  })}
                  {actions && actions.length &&
                    <TableCell className={classes.actions}>
                      {actions.map(action => (
                        <Button
                          key={action.key}
                          className={classes.actionBtn}
                          size="small"
                          color={action.color}
                          onClick={() => action.onClick(row)}
                        >
                          {action.title}
                        </Button>
                      ))}
                    </TableCell>}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        labelRowsPerPage="Количество строк на странице:"
        labelDisplayedRows={
          ({ from, to, count }) => (
           `${from}-${to === -1 ? count : to} из ${count !== -1 ? count : `больше, чем ${to}`}`
          )
        }
        rowsPerPageOptions={[10, 25, 50]}
        component="div"
        count={total}
        page={page - 1}
        onChangePage={(_, page) => onPageChange(page + 1)}
        rowsPerPage={limit}
        onChangeRowsPerPage={({ target: { value }}) => onLimitChange(value)}
      />
    </Paper>

  );
}

ResponsiveTable.propTypes = {
  items: PropTypes.array,
  columns: PropTypes.arrayOf(PropTypes.shape({
    key: PropTypes.string,
    title: PropTypes.string,
    getValue: PropTypes.func,
  })),
  actions: PropTypes.arrayOf(PropTypes.shape({
    key: PropTypes.string,
    title: PropTypes.string,
    onClick: PropTypes.func,
  })),
  page: PropTypes.number,
  onPageChange: PropTypes.func,
  limit: PropTypes.number,
  onLimitChange: PropTypes.func,
  total: PropTypes.number,
};
