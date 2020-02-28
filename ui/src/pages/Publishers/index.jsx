import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import Table from 'components/ResponsiveTable';
import { setHeader as setHeaderAction } from 'components/Header/actions';

import { convertDate } from 'lib/utils';

import {
  fetchPublishers as fetchPublishersAction,
  setFilters as setFiltersAction,
  mutatePublisher as mutatePublisherAction,
  deletePublisher as deletePublisherAction,
} from './actions';

import Form from './components/Form';


class Publishers extends React.Component {
  state = {
    form: {
      open: false,
      data: null,
    },
  };

  columns = [
    {
      key: 'name',
      title: 'Имя',
      sorting: 'name',
    },
    {
      key: 'airtime',
      title: 'Эфирное время',
      sorting: 'airtime',
    },
    {
      key: 'comment',
      title: 'Комментарий',
      sorting: 'comment',
    },
    {
      key: 'created_at',
      title: 'Дата создания',
      sorting: 'created_at',
      getValue: item => convertDate(item.created_at),
    },
  ];
  actions = [
    {
      key: 'edit',
      title: 'Редактировать',
      onClick: item => this.showForm(item),
      color: 'primary',
    },
    {
      key: 'delete',
      title: 'Удалить',
      onClick: item => this.deletePublisher(item),
      color: 'secondary',
    },
  ];

  componentDidMount() {
    const { fetchPublishers, setHeader } = this.props;
    setHeader({
      title: 'Рекламодатели',
      addBtn: {
        onClick: this.showForm,
        text: 'Добавить рекламодателя',
      },
      search: {
        placeholder: 'Поиск по рекламодателям',
        onSearch: (value) => {
          if (!value || 2 < value.length) {
            fetchPublishers();
          }
        },
      }
    });
    fetchPublishers();
  }

  componentWillUnmount() {
    const { setHeader } = this.props;
    setHeader({});
  }

  handleFiltersChange = (filters) => {
    const { setFilters, fetchPublishers } = this.props;
    setFilters(filters);
    fetchPublishers();
  };

  setPage = (page) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, page })
  };

  setLimit = (limit) => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, limit, page: 1 })
  };

  setSorting = sortBy => {
    const { filters } = this.props;
    this.handleFiltersChange({ ...filters, sort_by: sortBy })
  };

  showForm = (data=null) => {
    this.setState(({ form, ...rest }) => ({
      ...rest, form: { open: true, data }
    }))
  };

  hideForm = () => {
    this.setState(({ form, ...rest }) => ({
      ...rest, form: { open: false, data: null }
    }))
  };

  handleFormSubmit = (formData) => {
    const { form: { data } } = this.state;
    const { mutatePublisher } = this.props;
    mutatePublisher({...formData, id: data.id}, this.hideForm);
  };

  deletePublisher = (publisher) => {
    const { deletePublisher } = this.props;
    // TODO: make confirm dialog
    if (confirm(`Удалить рекламодателя ${publisher.name}?`)) {
      deletePublisher(publisher.id);
    }
  };

  render() {
    const { form } = this.state;
    const { publishers, filters, total } = this.props;
    return (
      <>
        {form.open &&
          <Form
            data={form.data}
            handleClose={this.hideForm}
            handleSubmit={this.handleFormSubmit} />
        }
        <Table
          items={publishers}
          columns={this.columns}
          actions={this.actions}
          sorting={filters.sort_by}
          onSortingChange={this.setSorting}
          page={filters.page}
          onPageChange={this.setPage}
          limit={filters.limit}
          onLimitChange={this.setLimit}
          total={total} />
      </>
    );
  }
}

Publishers.propTypes = {
  publishers: PropTypes.array.isRequired,
  isLoading: PropTypes.bool.isRequired,
  filters: PropTypes.object.isRequired,
  total: PropTypes.number.isRequired,
  fetchPublishers: PropTypes.func.isRequired,
  setFilters: PropTypes.func.isRequired,
  deletePublisher: PropTypes.func.isRequired,
  setHeader: PropTypes.func.isRequired,
};

const mapStateToProps = ({ publishersReducer }) => ({ ...publishersReducer });

const mapDispatchToProps = {
  fetchPublishers: fetchPublishersAction,
  mutatePublisher: mutatePublisherAction,
  setFilters: setFiltersAction,
  deletePublisher: deletePublisherAction,
  setHeader: setHeaderAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(Publishers);
