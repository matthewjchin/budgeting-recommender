import React, { useState, useEffect } from 'react';
import { PlusCircle, TrendingUp, TrendingDown, DollarSign, PieChart, Calendar, Target, AlertCircle } from 'lucide-react';
import { LineChart, Line, PieChart as RePieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

export default function BudgetTracker() {
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState({});
  const [view, setView] = useState('dashboard');
  const [newTransaction, setNewTransaction] = useState({
    description: '',
    amount: '',
    category: 'Food',
    type: 'expense',
    date: new Date().toISOString().split('T')[0]
  });
  const [newBudget, setNewBudget] = useState({ category: 'Food', limit: '' });

  const categories = ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 'Healthcare', 'Education', 'Other'];

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const txResult = await window.storage.get('budget-transactions');
      const budgetResult = await window.storage.get('budget-limits');
      
      if (txResult) setTransactions(JSON.parse(txResult.value));
      if (budgetResult) setBudgets(JSON.parse(budgetResult.value));
    } catch (error) {
      console.log('No existing data found');
    }
  };

  const saveData = async (newTx, newBudgets) => {
    try {
      await window.storage.set('budget-transactions', JSON.stringify(newTx || transactions));
      await window.storage.set('budget-limits', JSON.stringify(newBudgets || budgets));
    } catch (error) {
      console.error('Save failed:', error);
    }
  };

  const addTransaction = () => {
    if (!newTransaction.description || !newTransaction.amount) return;
    
    const tx = {
      ...newTransaction,
      amount: parseFloat(newTransaction.amount),
      id: Date.now()
    };
    
    const updated = [tx, ...transactions];
    setTransactions(updated);
    saveData(updated, null);
    setNewTransaction({
      description: '',
      amount: '',
      category: 'Food',
      type: 'expense',
      date: new Date().toISOString().split('T')[0]
    });
  };

  const setBudgetLimit = () => {
    if (!newBudget.limit) return;
    
    const updated = {
      ...budgets,
      [newBudget.category]: parseFloat(newBudget.limit)
    };
    setBudgets(updated);
    saveData(null, updated);
    setNewBudget({ category: 'Food', limit: '' });
  };

  const deleteTransaction = (id) => {
    const updated = transactions.filter(t => t.id !== id);
    setTransactions(updated);
    saveData(updated, null);
  };

  const currentMonth = new Date().toISOString().slice(0, 7);
  const monthTransactions = transactions.filter(t => t.date.startsWith(currentMonth));

  const totalIncome = monthTransactions
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0);

  const totalExpenses = monthTransactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0);

  const balance = totalIncome - totalExpenses;

  const categorySpending = categories.map(cat => {
    const spent = monthTransactions
      .filter(t => t.category === cat && t.type === 'expense')
      .reduce((sum, t) => sum + t.amount, 0);
    return { category: cat, spent, budget: budgets[cat] || 0 };
  }).filter(c => c.spent > 0 || c.budget > 0);

  const pieData = categorySpending.map(c => ({
    name: c.category,
    value: c.spent
  }));

  const last7Days = [...Array(7)].map((_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (6 - i));
    return d.toISOString().split('T')[0];
  });

  const trendData = last7Days.map(date => ({
    date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    expenses: transactions
      .filter(t => t.date === date && t.type === 'expense')
      .reduce((sum, t) => sum + t.amount, 0),
    income: transactions
      .filter(t => t.date === date && t.type === 'income')
      .reduce((sum, t) => sum + t.amount, 0)
  }));

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-4">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Budget Tracker Pro
          </h1>
          <p className="text-slate-300">Take control of your finances</p>
        </header>

        <nav className="flex gap-2 mb-6 flex-wrap">
          {['dashboard', 'transactions', 'budgets', 'analytics'].map(v => (
            <button
              key={v}
              onClick={() => setView(v)}
              className={`px-6 py-2 rounded-lg font-medium transition-all ${
                view === v
                  ? 'bg-gradient-to-r from-blue-500 to-purple-500 shadow-lg'
                  : 'bg-white/10 hover:bg-white/20'
              }`}
            >
              {v.charAt(0).toUpperCase() + v.slice(1)}
            </button>
          ))}
        </nav>

        {view === 'dashboard' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 backdrop-blur rounded-xl p-6 border border-green-500/30">
                <div className="flex items-center gap-3 mb-2">
                  <TrendingUp className="text-green-400" size={24} />
                  <span className="text-slate-300">Income</span>
                </div>
                <div className="text-3xl font-bold">${totalIncome.toFixed(2)}</div>
              </div>
              
              <div className="bg-gradient-to-br from-red-500/20 to-red-600/20 backdrop-blur rounded-xl p-6 border border-red-500/30">
                <div className="flex items-center gap-3 mb-2">
                  <TrendingDown className="text-red-400" size={24} />
                  <span className="text-slate-300">Expenses</span>
                </div>
                <div className="text-3xl font-bold">${totalExpenses.toFixed(2)}</div>
              </div>
              
              <div className={`bg-gradient-to-br ${balance >= 0 ? 'from-blue-500/20 to-blue-600/20 border-blue-500/30' : 'from-orange-500/20 to-orange-600/20 border-orange-500/30'} backdrop-blur rounded-xl p-6 border`}>
                <div className="flex items-center gap-3 mb-2">
                  <DollarSign className={balance >= 0 ? 'text-blue-400' : 'text-orange-400'} size={24} />
                  <span className="text-slate-300">Balance</span>
                </div>
                <div className="text-3xl font-bold">${balance.toFixed(2)}</div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <TrendingUp size={20} />
                  7-Day Trend
                </h2>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
                    <XAxis dataKey="date" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
                      labelStyle={{ color: '#e2e8f0' }}
                    />
                    <Legend />
                    <Line type="monotone" dataKey="income" stroke="#10b981" strokeWidth={2} />
                    <Line type="monotone" dataKey="expenses" stroke="#ef4444" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <Target size={20} />
                  Budget Status
                </h2>
                <div className="space-y-3">
                  {categorySpending.slice(0, 5).map(cat => {
                    const percent = cat.budget > 0 ? (cat.spent / cat.budget) * 100 : 0;
                    const isOver = percent > 100;
                    
                    return (
                      <div key={cat.category}>
                        <div className="flex justify-between text-sm mb-1">
                          <span>{cat.category}</span>
                          <span className={isOver ? 'text-red-400' : 'text-slate-300'}>
                            ${cat.spent.toFixed(0)} / ${cat.budget.toFixed(0)}
                          </span>
                        </div>
                        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                          <div
                            className={`h-full ${isOver ? 'bg-red-500' : 'bg-green-500'} transition-all`}
                            style={{ width: `${Math.min(percent, 100)}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-4">Recent Transactions</h2>
              <div className="space-y-2">
                {transactions.slice(0, 5).map(tx => (
                  <div key={tx.id} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                    <div>
                      <div className="font-medium">{tx.description}</div>
                      <div className="text-sm text-slate-400">{tx.category} • {tx.date}</div>
                    </div>
                    <div className={`font-bold ${tx.type === 'income' ? 'text-green-400' : 'text-red-400'}`}>
                      {tx.type === 'income' ? '+' : '-'}${tx.amount.toFixed(2)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {view === 'transactions' && (
          <div className="space-y-6">
            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <PlusCircle size={20} />
                Add Transaction
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                <input
                  type="text"
                  placeholder="Description"
                  value={newTransaction.description}
                  onChange={(e) => setNewTransaction({...newTransaction, description: e.target.value})}
                  className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:border-blue-500"
                />
                <input
                  type="number"
                  placeholder="Amount"
                  value={newTransaction.amount}
                  onChange={(e) => setNewTransaction({...newTransaction, amount: e.target.value})}
                  className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:border-blue-500"
                />
                <select
                  value={newTransaction.category}
                  onChange={(e) => setNewTransaction({...newTransaction, category: e.target.value})}
                  className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:border-blue-500"
                >
                  {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
                </select>
                <select
                  value={newTransaction.type}
                  onChange={(e) => setNewTransaction({...newTransaction, type: e.target.value})}
                  className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:border-blue-500"
                >
                  <option value="expense">Expense</option>
                  <option value="income">Income</option>
                </select>
                <button
                  onClick={addTransaction}
                  className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-medium hover:shadow-lg transition-all"
                >
                  Add
                </button>
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-4">All Transactions</h2>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {transactions.map(tx => (
                  <div key={tx.id} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                    <div className="flex-1">
                      <div className="font-medium">{tx.description}</div>
                      <div className="text-sm text-slate-400">{tx.category} • {tx.date}</div>
                    </div>
                    <div className={`font-bold mr-4 ${tx.type === 'income' ? 'text-green-400' : 'text-red-400'}`}>
                      {tx.type === 'income' ? '+' : '-'}${tx.amount.toFixed(2)}
                    </div>
                    <button
                      onClick={() => deleteTransaction(tx.id)}
                      className="px-3 py-1 bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {view === 'budgets' && (
          <div className="space-y-6">
            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Target size={20} />
                Set Budget Limits
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <select
                  value={newBudget.category}
                  onChange={(e) => setNewBudget({...newBudget, category: e.target.value})}
                  className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:border-blue-500"
                >
                  {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
                </select>
                <input
                  type="number"
                  placeholder="Monthly limit"
                  value={newBudget.limit}
                  onChange={(e) => setNewBudget({...newBudget, limit: e.target.value})}
                  className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:border-blue-500"
                />
                <button
                  onClick={setBudgetLimit}
                  className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-medium hover:shadow-lg transition-all"
                >
                  Set Limit
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {categorySpending.map(cat => {
                const percent = cat.budget > 0 ? (cat.spent / cat.budget) * 100 : 0;
                const isOver = percent > 100;
                const isWarning = percent > 80 && !isOver;
                
                return (
                  <div
                    key={cat.category}
                    className={`bg-white/5 backdrop-blur rounded-xl p-6 border ${
                      isOver ? 'border-red-500/50' : isWarning ? 'border-yellow-500/50' : 'border-white/10'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold">{cat.category}</h3>
                      {isOver && <AlertCircle className="text-red-400" size={20} />}
                      {isWarning && <AlertCircle className="text-yellow-400" size={20} />}
                    </div>
                    <div className="mb-2">
                      <div className="flex justify-between text-sm mb-1">
                        <span>Spent</span>
                        <span className={isOver ? 'text-red-400 font-bold' : ''}>
                          ${cat.spent.toFixed(2)} / ${cat.budget.toFixed(2)}
                        </span>
                      </div>
                      <div className="h-3 bg-white/10 rounded-full overflow-hidden">
                        <div
                          className={`h-full transition-all ${
                            isOver ? 'bg-red-500' : isWarning ? 'bg-yellow-500' : 'bg-green-500'
                          }`}
                          style={{ width: `${Math.min(percent, 100)}%` }}
                        />
                      </div>
                    </div>
                    <div className="text-sm text-slate-400">
                      {cat.budget > cat.spent ? (
                        `$${(cat.budget - cat.spent).toFixed(2)} remaining`
                      ) : (
                        `$${(cat.spent - cat.budget).toFixed(2)} over budget`
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {view === 'analytics' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <PieChart size={20} />
                  Spending by Category
                </h2>
                <ResponsiveContainer width="100%" height={300}>
                  <RePieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }} />
                  </RePieChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
                <h2 className="text-xl font-semibold mb-4">Monthly Summary</h2>
                <div className="space-y-4">
                  <div className="p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
                    <div className="text-sm text-slate-300 mb-1">Total Income</div>
                    <div className="text-2xl font-bold text-green-400">${totalIncome.toFixed(2)}</div>
                  </div>
                  <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
                    <div className="text-sm text-slate-300 mb-1">Total Expenses</div>
                    <div className="text-2xl font-bold text-red-400">${totalExpenses.toFixed(2)}</div>
                  </div>
                  <div className={`p-4 ${balance >= 0 ? 'bg-blue-500/10 border-blue-500/30' : 'bg-orange-500/10 border-orange-500/30'} border rounded-lg`}>
                    <div className="text-sm text-slate-300 mb-1">Net Balance</div>
                    <div className={`text-2xl font-bold ${balance >= 0 ? 'text-blue-400' : 'text-orange-400'}`}>
                      ${balance.toFixed(2)}
                    </div>
                  </div>
                  <div className="p-4 bg-purple-500/10 border border-purple-500/30 rounded-lg">
                    <div className="text-sm text-slate-300 mb-1">Savings Rate</div>
                    <div className="text-2xl font-bold text-purple-400">
                      {totalIncome > 0 ? ((balance / totalIncome) * 100).toFixed(1) : 0}%
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-4">Top Expenses</h2>
              <div className="space-y-2">
                {transactions
                  .filter(t => t.type === 'expense')
                  .sort((a, b) => b.amount - a.amount)
                  .slice(0, 10)
                  .map(tx => (
                    <div key={tx.id} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                      <div>
                        <div className="font-medium">{tx.description}</div>
                        <div className="text-sm text-slate-400">{tx.category} • {tx.date}</div>
                      </div>
                      <div className="text-red-400 font-bold">${tx.amount.toFixed(2)}</div>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}