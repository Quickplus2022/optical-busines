import React from 'react';
import { Link } from 'react-router-dom';
import { PlusIcon, BuildingOfficeIcon, ChartBarIcon, CurrencyDollarIcon } from '@heroicons/react/24/outline';

const Dashboard: React.FC = () => {
  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Bem-vindo ao seu painel de controle de planejamento de negócios
        </p>
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <Link
          to="/businesses/new"
          className="card hover:shadow-md transition-shadow cursor-pointer"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <PlusIcon className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Novo Negócio</h3>
              <p className="text-sm text-gray-500">Criar um novo plano</p>
            </div>
          </div>
        </Link>

        <Link
          to="/businesses"
          className="card hover:shadow-md transition-shadow cursor-pointer"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <BuildingOfficeIcon className="h-8 w-8 text-success-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Meus Negócios</h3>
              <p className="text-sm text-gray-500">Gerenciar planos</p>
            </div>
          </div>
        </Link>

        <Link
          to="/financial"
          className="card hover:shadow-md transition-shadow cursor-pointer"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CurrencyDollarIcon className="h-8 w-8 text-warning-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Financeiro</h3>
              <p className="text-sm text-gray-500">Análises financeiras</p>
            </div>
          </div>
        </Link>

        <Link
          to="/reports"
          className="card hover:shadow-md transition-shadow cursor-pointer"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <ChartBarIcon className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Relatórios</h3>
              <p className="text-sm text-gray-500">Gerar relatórios</p>
            </div>
          </div>
        </Link>
      </div>

      {/* Recent activities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Atividades Recentes</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Sistema iniciado</span>
              <span className="text-xs text-gray-400">Agora</span>
            </div>
            <div className="text-sm text-gray-500">
              Nenhuma atividade recente ainda.
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Próximos Passos</h3>
          <div className="space-y-3">
            <div className="flex items-start">
              <div className="flex-shrink-0 w-2 h-2 bg-primary-600 rounded-full mt-2"></div>
              <div className="ml-3">
                <p className="text-sm text-gray-600">
                  Crie seu primeiro negócio para começar o planejamento
                </p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 w-2 h-2 bg-gray-300 rounded-full mt-2"></div>
              <div className="ml-3">
                <p className="text-sm text-gray-400">
                  Adicione fornecedores e produtos/serviços
                </p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 w-2 h-2 bg-gray-300 rounded-full mt-2"></div>
              <div className="ml-3">
                <p className="text-sm text-gray-400">
                  Configure custos fixos e variáveis
                </p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 w-2 h-2 bg-gray-300 rounded-full mt-2"></div>
              <div className="ml-3">
                <p className="text-sm text-gray-400">
                  Gere seu primeiro relatório
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;