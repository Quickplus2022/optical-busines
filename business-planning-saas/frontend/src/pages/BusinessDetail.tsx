import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { businessApi, Business } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const BusinessDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [business, setBusiness] = useState<Business | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      loadBusiness();
    }
  }, [id]);

  const loadBusiness = async () => {
    try {
      const response = await businessApi.get(id!);
      setBusiness(response.data);
    } catch (err: any) {
      setError('Erro ao carregar negócio');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error || !business) {
    return (
      <div className="p-6">
        <div className="bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded">
          {error || 'Negócio não encontrado'}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{business.name}</h1>
        <p className="mt-2 text-gray-600">{business.description}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Informações Básicas</h2>
          <div className="space-y-3">
            <div>
              <span className="text-sm font-medium text-gray-500">Segmento:</span>
              <p className="text-gray-900">{business.segment}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-500">Indústria:</span>
              <p className="text-gray-900">{business.industry}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-500">Tipo:</span>
              <p className="text-gray-900">{business.business_type}</p>
            </div>
            {business.cnpj && (
              <div>
                <span className="text-sm font-medium text-gray-500">CNPJ:</span>
                <p className="text-gray-900">{business.cnpj}</p>
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Localização</h2>
          <div className="space-y-3">
            {business.address && (
              <div>
                <span className="text-sm font-medium text-gray-500">Endereço:</span>
                <p className="text-gray-900">{business.address}</p>
              </div>
            )}
            {business.city && (
              <div>
                <span className="text-sm font-medium text-gray-500">Cidade:</span>
                <p className="text-gray-900">{business.city}</p>
              </div>
            )}
            {business.state && (
              <div>
                <span className="text-sm font-medium text-gray-500">Estado:</span>
                <p className="text-gray-900">{business.state}</p>
              </div>
            )}
          </div>
        </div>

        {business.target_audience && (
          <div className="card lg:col-span-2">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Público-alvo</h2>
            <p className="text-gray-900">{business.target_audience}</p>
          </div>
        )}
      </div>

      <div className="mt-8">
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Próximos Passos</h2>
          <p className="text-gray-600 mb-4">
            Configure seu negócio adicionando fornecedores, produtos/serviços e análises financeiras.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="btn-primary" disabled>
              Adicionar Fornecedores
            </button>
            <button className="btn-primary" disabled>
              Configurar Financeiro
            </button>
            <button className="btn-primary" disabled>
              Análise Estratégica
            </button>
          </div>
          <p className="text-sm text-gray-500 mt-2">
            * Funcionalidades em desenvolvimento
          </p>
        </div>
      </div>
    </div>
  );
};

export default BusinessDetail;