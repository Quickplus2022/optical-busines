import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { businessApi, BusinessCreate } from '../services/api';

interface BusinessForm extends BusinessCreate {
  // Adicionar campos do formulário se necessário
}

const CreateBusiness: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<BusinessForm>();

  const onSubmit = async (data: BusinessForm) => {
    setIsLoading(true);
    setError('');
    
    try {
      const response = await businessApi.create(data);
      navigate(`/businesses/${response.data.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao criar negócio');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Criar Novo Negócio</h1>
          <p className="mt-2 text-gray-600">
            Preencha as informações básicas do seu negócio para começar o planejamento
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {error && (
            <div className="bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Informações Básicas</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="md:col-span-2">
                <label htmlFor="name" className="form-label">
                  Nome do Negócio *
                </label>
                <input
                  id="name"
                  type="text"
                  className="form-input"
                  {...register('name', {
                    required: 'Nome do negócio é obrigatório',
                    minLength: {
                      value: 3,
                      message: 'Nome deve ter pelo menos 3 caracteres'
                    }
                  })}
                />
                {errors.name && (
                  <p className="mt-1 text-sm text-danger-600">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="segment" className="form-label">
                  Segmento *
                </label>
                <select
                  id="segment"
                  className="form-input"
                  {...register('segment', { required: 'Segmento é obrigatório' })}
                >
                  <option value="">Selecione um segmento</option>
                  <option value="Comércio">Comércio</option>
                  <option value="Serviços">Serviços</option>
                  <option value="Indústria">Indústria</option>
                  <option value="Tecnologia">Tecnologia</option>
                  <option value="Alimentação">Alimentação</option>
                  <option value="Educação">Educação</option>
                  <option value="Saúde">Saúde</option>
                  <option value="Consultoria">Consultoria</option>
                  <option value="Outros">Outros</option>
                </select>
                {errors.segment && (
                  <p className="mt-1 text-sm text-danger-600">{errors.segment.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="industry" className="form-label">
                  Indústria *
                </label>
                <input
                  id="industry"
                  type="text"
                  className="form-input"
                  placeholder="Ex: Desenvolvimento de Software"
                  {...register('industry', { required: 'Indústria é obrigatória' })}
                />
                {errors.industry && (
                  <p className="mt-1 text-sm text-danger-600">{errors.industry.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="business_type" className="form-label">
                  Tipo de Empresa *
                </label>
                <select
                  id="business_type"
                  className="form-input"
                  {...register('business_type', { required: 'Tipo de empresa é obrigatório' })}
                >
                  <option value="">Selecione o tipo</option>
                  <option value="MEI">MEI</option>
                  <option value="ME">ME - Microempresa</option>
                  <option value="EPP">EPP - Empresa de Pequeno Porte</option>
                  <option value="Ltda">Ltda</option>
                  <option value="SA">SA</option>
                  <option value="Outros">Outros</option>
                </select>
                {errors.business_type && (
                  <p className="mt-1 text-sm text-danger-600">{errors.business_type.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="cnpj" className="form-label">
                  CNPJ
                </label>
                <input
                  id="cnpj"
                  type="text"
                  className="form-input"
                  placeholder="00.000.000/0001-00"
                  {...register('cnpj')}
                />
              </div>

              <div className="md:col-span-2">
                <label htmlFor="description" className="form-label">
                  Descrição
                </label>
                <textarea
                  id="description"
                  rows={3}
                  className="form-input"
                  placeholder="Descreva brevemente o seu negócio..."
                  {...register('description')}
                />
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Localização</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="md:col-span-2">
                <label htmlFor="address" className="form-label">
                  Endereço
                </label>
                <input
                  id="address"
                  type="text"
                  className="form-input"
                  {...register('address')}
                />
              </div>

              <div>
                <label htmlFor="city" className="form-label">
                  Cidade
                </label>
                <input
                  id="city"
                  type="text"
                  className="form-input"
                  {...register('city')}
                />
              </div>

              <div>
                <label htmlFor="state" className="form-label">
                  Estado
                </label>
                <input
                  id="state"
                  type="text"
                  className="form-input"
                  {...register('state')}
                />
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Mercado</h2>
            
            <div className="space-y-6">
              <div>
                <label htmlFor="target_audience" className="form-label">
                  Público-alvo
                </label>
                <textarea
                  id="target_audience"
                  rows={3}
                  className="form-input"
                  placeholder="Descreva o seu público-alvo..."
                  {...register('target_audience')}
                />
              </div>

              <div>
                <label htmlFor="market_size" className="form-label">
                  Tamanho do Mercado
                </label>
                <select
                  id="market_size"
                  className="form-input"
                  {...register('market_size')}
                >
                  <option value="">Selecione o tamanho</option>
                  <option value="Local">Local</option>
                  <option value="Regional">Regional</option>
                  <option value="Nacional">Nacional</option>
                  <option value="Internacional">Internacional</option>
                </select>
              </div>
            </div>
          </div>

          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate('/businesses')}
              className="btn-secondary"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Criando...' : 'Criar Negócio'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateBusiness;