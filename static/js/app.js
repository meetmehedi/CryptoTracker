document.addEventListener('DOMContentLoaded', () => {

    // Login Form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await res.json();
                if (res.ok) {
                    window.location.href = data.redirect;
                } else {
                    alert(data.error || 'Login failed');
                }
            } catch (err) {
                console.error(err);
                alert('An error occurred');
            }
        });
    }

    // Register Form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const res = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, password })
                });
                const data = await res.json();
                if (res.ok) {
                    alert('Registration successful! Please login.');
                    window.location.href = '/login_page';
                } else {
                    alert(data.error || 'Registration failed');
                }
            } catch (err) {
                console.error(err);
                alert('An error occurred');
            }
        });
    }

    // Dashboard Only - Fetch Holdings & Activity
    const holdingsTable = document.getElementById('holdings');
    if (holdingsTable) {
        fetchHoldings();
        fetchTransactions();
        populateCoinSelect();

        // Auto-refresh every 30 seconds
        setInterval(() => {
            fetchHoldings();
            fetchTransactions();
        }, 30000);
    }

    // Transaction Form
    const txnForm = document.getElementById('txnForm');
    if (txnForm) {
        txnForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const coin_id = document.getElementById('coin_id').value;
            const type = document.getElementById('txn_type').value;
            const quantity = document.getElementById('quantity').value;
            const price = document.getElementById('price').value;

            try {
                const res = await fetch('/transaction', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        coin_id,
                        type,
                        quantity,
                        price_at_time: price
                    })
                });
                const data = await res.json();
                if (res.ok) {
                    alert('Transaction added!');
                    closeModal();
                    fetchHoldings();
                    fetchTransactions();
                } else {
                    alert(data.error || 'Transaction failed');
                }
            } catch (err) {
                console.error(err);
                alert('An error occurred');
            }
        });
    }
});

async function fetchHoldings() {
    try {
        const res = await fetch("/get_holdings");
        if (res.status === 401) {
            window.location.href = '/login_page';
            return;
        }
        const data = await res.json();
        const tbody = document.getElementById("holdings");
        tbody.innerHTML = "";

        let portfolioTotalValue = 0;
        let portfolioTotalPnL = 0;

        data.forEach((row) => {
            const symbol = row[0];
            const name = row[1];
            const quantity = parseFloat(row[2]);
            const currentPrice = parseFloat(row[3] || 0);
            const avgBuyPrice = parseFloat(row[4] || 0);

            const currentValue = quantity * currentPrice;
            const costBasis = quantity * avgBuyPrice;
            const profitLoss = currentValue - costBasis;
            const isProfit = profitLoss >= 0;

            portfolioTotalValue += currentValue;
            portfolioTotalPnL += profitLoss;

            // Format price for display (show more decimals if < 1)
            const displayPrice = currentPrice < 1 ? currentPrice.toFixed(6) : currentPrice.toFixed(2);
            const displayPnL = profitLoss.toFixed(2);
            const pnlColor = isProfit ? "text-emerald-400" : "text-red-400";
            const pnlSign = isProfit ? "+" : "";

            const tr = document.createElement("tr");
            tr.className = "hover:bg-white/10 transition-colors";
            tr.innerHTML = `
                <td class="border-b border-white/10 px-8 py-4 font-bold text-white">${symbol} <span class="text-xs font-normal text-gray-400 block">${name}</span></td>
                <td class="border-b border-white/10 px-8 py-4 text-white">${quantity.toFixed(4)}</td>
                <td class="border-b border-white/10 px-8 py-4 text-white">
                    <div>$${displayPrice}</div>
                    <div class="text-xs text-gray-400">Avg: $${avgBuyPrice.toFixed(2)}</div>
                </td>
                <td class="border-b border-white/10 px-8 py-4 text-white">
                    <div>$${currentValue.toFixed(2)}</div>
                    <div class="text-xs ${pnlColor} font-bold">${pnlSign}$${displayPnL}</div>
                </td>
            `;
            tbody.appendChild(tr);
        });

        // Update Total Summary
        const totalValueEl = document.getElementById('total-value');
        const totalPnLEl = document.getElementById('total-pnl');

        if (totalValueEl && totalPnLEl) {
            totalValueEl.textContent = `$${portfolioTotalValue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
            totalPnLEl.textContent = (portfolioTotalPnL >= 0 ? "+" : "") + `$${portfolioTotalPnL.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
            totalPnLEl.className = `text-2xl font-bold ${portfolioTotalPnL >= 0 ? 'text-emerald-400' : 'text-red-400'}`;
        }
    } catch (err) {
        console.error(err);
    }
}

async function fetchTransactions() {
    try {
        const res = await fetch("/api/transactions");
        const data = await res.json();
        const tbody = document.getElementById("activity");
        tbody.innerHTML = "";

        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" class="px-8 py-4 text-center text-gray-400">No recent activity</td></tr>`;
            return;
        }

        data.forEach((row) => {
            // Row: type, quantity, price_at_time, txn_date, symbol, name
            const type = row[0];
            const quantity = parseFloat(row[1]);
            const price = parseFloat(row[2]);
            // Format Date and Time in BDT
            const date = new Date(row[3]);
            const dateStr = date.toLocaleDateString('en-GB', { timeZone: 'Asia/Dhaka' });
            const timeStr = date.toLocaleTimeString('en-GB', { timeZone: 'Asia/Dhaka', hour: '2-digit', minute: '2-digit' });

            const symbol = row[4];
            const name = row[5];

            const typeColor = type === 'buy' ? 'text-emerald-400' : 'text-red-400';
            const typeLabel = type.toUpperCase();

            const tr = document.createElement("tr");
            tr.className = "hover:bg-white/10 transition-colors";
            tr.innerHTML = `
                <td class="border-b border-white/10 px-8 py-4 font-bold text-white">${symbol} <span class="text-xs font-normal text-gray-400 block">${name}</span></td>
                <td class="border-b border-white/10 px-8 py-4 ${typeColor} font-bold">${typeLabel}</td>
                <td class="border-b border-white/10 px-8 py-4 text-white">${quantity.toFixed(4)}</td>
                <td class="border-b border-white/10 px-8 py-4 text-white">$${price.toFixed(2)}</td>
                <td class="border-b border-white/10 px-8 py-4">
                    <div class="text-white text-sm">${dateStr}</div>
                    <div class="text-gray-500 text-xs">${timeStr}</div>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
    }
}

async function populateCoinSelect() {
    try {
        const res = await fetch("/coins");
        const data = await res.json();
        const select = document.getElementById('coin_id');
        data.forEach(coin => {
            const option = document.createElement('option');
            option.value = coin[0]; // id
            option.textContent = `${coin[1]} - ${coin[2]}`; // symbol - name
            select.appendChild(option);
        });
    } catch (err) {
        console.error(err);
    }
}

function openModal() {
    document.getElementById('txnModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('txnModal').classList.add('hidden');
}
