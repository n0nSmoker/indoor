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
import TableSortLabel from '@material-ui/core/TableSortLabel';
import Button from '@material-ui/core/Button';


const useStyles = makeStyles({
  paper: {
    borderRadius: 5,
    cursor: 'default',
  },
  tableContainer: {
    backgroundColor: 'white',
    borderTopLeftRadius: 5,
    borderTopRightRadius: 5,
    maxHeight: 'calc(100vh - 230px)',  // TODO: fix it, make dynamic
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


function getSortObject(sorting) {
  if (!sorting) return {};

  const isDesc = sorting.charAt(0) === '-';
  return {
    direction: isDesc ? 'desc': 'asc',
    field: isDesc ? sorting.substr(1) : sorting,
  };
}


function RTHead({ classes, columns, hasActions, sorting, onSortingChange }) {
  const sort = getSortObject(sorting);
  const setSorting = field => () => {
    let isDesc = true;
    if (field === sort.field && sort.direction === 'desc') {
      isDesc = false;
    }
    onSortingChange(`${isDesc ? '-' : ''}${field}`);
  };
  return (
    <TableHead>
      <TableRow>
        <TableCell className={cn(classes.serial, classes.headCell)}>№ п/п</TableCell>
        {columns.map(column => {
          const isActive = column.sorting === sort.field;
          return (
            <TableCell key={column.key} className={classes.headCell}>
            {column.sorting
              && (
                <TableSortLabel
                  hideSortIcon
                  direction={sort.direction}
                  active={isActive}
                  onClick={setSorting(column.sorting)}
                >
                  {column.title}
                </TableSortLabel>
              )
              || column.title
            }
          </TableCell>
          );
        })}
        {hasActions &&
          <TableCell className={classes.headCell}>
            Действия
          </TableCell>}
      </TableRow>
    </TableHead>
  );
}


function RTBody({ actions, classes, columns, items }) {
  return (
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
  );
}


// TODO: make responsive
export default function ResponsiveTable({
  items,
  columns,
  actions,
  sorting,
  onSortingChange,
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
          <RTHead
            classes={classes}
            columns={columns}
            hasActions={Boolean(actions && actions.length)}
            sorting={sorting}
            onSortingChange={onSortingChange}
          />
          <RTBody
            actions={actions}
            classes={classes}
            columns={columns}
            items={items}
          />
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
    sorting: PropTypes.string,
    getValue: PropTypes.func,
  })),
  actions: PropTypes.arrayOf(PropTypes.shape({
    key: PropTypes.string,
    title: PropTypes.string,
    onClick: PropTypes.func,
  })),
  sorting: PropTypes.string,
  onSortingChange: PropTypes.func,
  page: PropTypes.number,
  onPageChange: PropTypes.func,
  limit: PropTypes.number,
  onLimitChange: PropTypes.func,
  total: PropTypes.number,
};
