import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import Table from '../../components/ResponsiveTable';
import { setHeader as setHeaderAction } from 'components/Header/actions';

import { convertDate } from 'lib/utils';
import {
  fetchContent as fetchContentAction,
  setFilters as setFiltersAction,
  mutateContent as mutateContentAction,
  deleteContent as deleteContentAction,
} from './actions.js';

import { contentPreview } from './helpers.js';
import Form from './components/Form';

const styles = theme => ({
  controls: {
    marginBottom: theme.spacing(2),
  },
});


class Content extends React.Component {
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
      key: 'preview',
      title: 'Предпросмотр',
      getValue: item => contentPreview(item.src),
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
      onClick: item => this.deleteContent(item),
      color: 'secondary',
    },
  ];

  componentDidMount() {
    const { fetchContent, setHeader } = this.props;
    setHeader({
      title: 'Контент',
      addBtn: {
        onClick: this.showForm,
        text: 'Добавить контент',
      },
      search: {
        placeholder: 'Поиск по контенту',
        onSearch: (value) => {
          if (!value || 2 < value.length) {
            fetchContent();
          }
        },
      },
    });
    fetchContent();
  }

  componentWillUnmount() {
    const { setHeader } = this.props;
    setHeader({});
  }

  handleFiltersChange = (filters) => {
    const { setFilters, fetchContent } = this.props;
    setFilters(filters);
    fetchContent();
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
    const { mutateContent } = this.props;
    const newFormData = new FormData();
    newFormData.set('comment', formData.comment);
    newFormData.append('file', formData.file);
    mutateContent({formData: newFormData, id: data.id}, this.hideForm);
  };

  deleteContent = (content) => {
    const { deleteContent } = this.props;
    // TODO: make confirm dialog
    if (confirm(`Удалить контент ${content.name}`)) {
      deleteContent(content.id);
    }
  };

  render() {
    const { form } = this.state;
    const { content, filters, total } = this.props;
    return (
      <>
        {form.open &&
          <Form
            data={form.data}
            handleClose={this.hideForm}
            handleSubmit={this.handleFormSubmit} />
        }
        <Table
          items={content}
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

Content.propTypes = {
  content: PropTypes.array.isRequired,
  isLoading: PropTypes.bool.isRequired,
  filters: PropTypes.object.isRequired,
  total: PropTypes.number.isRequired,
  fetchContent: PropTypes.func.isRequired,
  setFilters: PropTypes.func.isRequired,
  mutateContent: PropTypes.func.isRequired,
  deleteContent: PropTypes.func.isRequired,
  setHeader: PropTypes.func.isRequired,
};

const mapStateToProps = ({ contentReducer }) => ({ ...contentReducer });

const mapDispatchToProps = {
  fetchContent: fetchContentAction,
  setFilters: setFiltersAction,
  mutateContent: mutateContentAction,
  deleteContent: deleteContentAction,
  setHeader: setHeaderAction,
};

export default connect(mapStateToProps, mapDispatchToProps)(Content);
