import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { PlusIcon, EyeIcon } from '@heroicons/react/24/outline';
import { businessApi, Business } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const BusinessList: React.FC = () => {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadBusinesses();
  }, []);

  const loadBusinesses = async () => {
    try {
      const response = await businessApi.list();
      setBusinesses(response.data);
    } catch (err: any) {
      setError('Erro ao carregar negócios');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Meus Negócios</h1>
          <p className="mt-2 text-gray-600">
            Gerencie todos os seus planos de negócio
          </p>
        </div>
        <Link
          to="/businesses/new"
          className="btn-primary inline-flex items-center"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Novo Negócio
        </Link>
      </div>

      {error && (
        <div className="bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {businesses.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhum negócio cadastrado
          </h3>
          <p className="text-gray-500 mb-6">
            Comece criando seu primeiro plano de negócio
          </p>
          <Link
            to="/businesses/new"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Criar Primeiro Negócio
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {businesses.map((business) => (
            <div key={business.id} className="card hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-semibold text-gray-900 truncate">
                  {business.name}
                </h3>
                <Link
                  to={`/businesses/${business.id}`}
                  className="text-primary-600 hover:text-primary-500"
                >
                  <EyeIcon className="h-5 w-5" />
                </Link>
              </div>
              
              <div className="space-y-2 mb-4">
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-medium">Segmento:</span>
                  <span className="ml-2">{business.segment}</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-medium">Indústria:</span>
                  <span className="ml-2">{business.industry}</span>
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-medium">Tipo:</span>
                  <span className="ml-2">{business.business_type}</span>
                </div>
              </div>

              {business.description && (
                <p className="text-sm text-gray-500 mb-4 line-clamp-2">
                  {business.description}
                </p>
              )}

              <div className="flex justify-between items-center pt-4 border-t border-gray-200">
                <span className="text-xs text-gray-400">
                  Criado em {new Date(business.created_at).toLocaleDateString('pt-BR')}
                </span>
                <Link
                  to={`/businesses/${business.id}`}
                  className="btn btn-sm bg-primary-50 text-primary-700 hover:bg-primary-100"
                >
                  Ver Detalhes
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BusinessList;