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

                const contentType = res.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    const data = await res.json();
                    if (res.ok) {
                        window.location.href = data.redirect;
                    } else {
                        alert(data.error || 'Login failed');
                    }
                } else {
                    const text = await res.text();
                    console.error("Non-JSON response:", text);
                    alert('Server Error (Check logs): ' + text.substring(0, 100));
                }
            } catch (err) {
                console.error(err);
                alert('Network Error: ' + err.message);
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

                const contentType = res.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    const data = await res.json();
                    if (res.ok) {
                        alert('Registration successful! Please login.');
                        window.location.href = '/login_page';
                    } else {
                        alert(data.error || 'Registration failed');
                    }
                } else {
                    const text = await res.text();
                    console.error("Non-JSON response:", text);
                    alert('Server Error (Check logs): ' + text.substring(0, 100));
                }
            } catch (err) {
                console.error(err);
                alert('Network Error: ' + err.message);
            }
        });
    }

    // Dashboard Only - Fetch Holdings & Activity & Alerts
    const holdingsTable = document.getElementById('holdings');
    if (holdingsTable) {
        fetchHoldings();
        fetchTransactions();
        fetchAlerts();
        populateCoinSelect();

        // Auto-refresh every 30 seconds
        setInterval(() => {
            fetchHoldings();
            fetchTransactions();
            fetchAlerts();
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
                alert('An error occurred: ' + err.message);
            }
        });
    }

    // Alert Form
    const alertForm = document.getElementById('alertForm');
    if (alertForm) {
        alertForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const coin_id = document.getElementById('alert_coin_id').value;
            const condition_type = document.getElementById('condition_type').value;
            const target_value = document.getElementById('target_price').value;

            try {
                const res = await fetch('/api/alerts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ coin_id, condition_type, target_value })
                });
                if (res.ok) {
                    alert('Alert set!');
                    closeAlertModal();
                    fetchAlerts();
                } else {
                    alert('Failed to set alert');
                }
            } catch (err) {
                console.error(err);
                alert('An error occurred: ' + err.message);
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
            try {
                // Row: type, quantity, price_at_time, txn_date, symbol, name
                const type = row[0];
                const quantity = parseFloat(row[1]);
                const price = parseFloat(row[2]);

                let bdtDate = "Invalid Date";
                let bdtTime = "";
                let usDate = "";
                let usTime = "";

                try {
                    const date = new Date(row[3]);
                    bdtDate = date.toLocaleDateString('en-GB', { timeZone: 'Asia/Dhaka' });
                    bdtTime = date.toLocaleTimeString('en-GB', { timeZone: 'Asia/Dhaka', hour: '2-digit', minute: '2-digit' });
                    usDate = date.toLocaleDateString('en-US', { timeZone: 'America/New_York' });
                    usTime = date.toLocaleTimeString('en-US', { timeZone: 'America/New_York', hour: '2-digit', minute: '2-digit' });
                } catch (e) {
                    console.error("Date parsing error:", e);
                    bdtDate = row[3]; // Fallback to raw string
                }

                const symbol = row[4];
                const name = row[5];

                const typeColor = type === 'buy' ? 'text-emerald-400' : 'text-red-400';
                const typeLabel = type ? type.toUpperCase() : 'UNKNOWN';

                const tr = document.createElement("tr");
                tr.className = "hover:bg-white/10 transition-colors";
                tr.innerHTML = `
                    <td class="border-b border-white/10 px-8 py-4 font-bold text-white">${symbol} <span class="text-xs font-normal text-gray-400 block">${name}</span></td>
                    <td class="border-b border-white/10 px-8 py-4 ${typeColor} font-bold">${typeLabel}</td>
                    <td class="border-b border-white/10 px-8 py-4 text-white">${(quantity || 0).toFixed(4)}</td>
                    <td class="border-b border-white/10 px-8 py-4 text-white">$${(price || 0).toFixed(2)}</td>
                    <td class="border-b border-white/10 px-8 py-4">
                        <div class="text-white text-sm">${bdtDate} ${bdtTime} (BDT)</div>
                        <div class="text-gray-500 text-xs">${usDate} ${usTime} (US)</div>
                    </td>
                `;
                tbody.appendChild(tr);
            } catch (err) {
                console.error("Error rendering transaction row:", err, row);
            }
        });
    } catch (err) {
        console.error(err);
    }
}

async function fetchAlerts() {
    try {
        const res = await fetch("/api/alerts");
        const alerts = await res.json();
        const container = document.getElementById("alerts-container");
        const section = document.getElementById("alerts-section");

        if (alerts.length === 0) {
            section.classList.add("hidden");
            return;
        }

        section.classList.remove("hidden");
        container.innerHTML = "";

        alerts.forEach((alert) => {
            // alert: id, symbol, name, condition_type, target_value, status, current_price, coin_id
            const [id, symbol, name, condition, target, status, current, coin_id] = alert;
            const targetPrice = parseFloat(target);
            const currentPrice = parseFloat(current || 0);

            let isTriggered = false;
            if (condition === 'ABOVE' && currentPrice >= targetPrice) isTriggered = true;
            if (condition === 'BELOW' && currentPrice <= targetPrice) isTriggered = true;

            const card = document.createElement("div");
            card.className = `glass-card p-6 rounded-2xl relative border ${isTriggered ? 'border-red-500/50 shadow-[0_0_20px_rgba(239,68,68,0.2)]' : 'border-white/10'}`;

            card.innerHTML = `
                <div class="flex justify-between items-start mb-4">
                    <div>
                        <span class="text-white font-bold block">${symbol}</span>
                        <span class="text-xs text-gray-400">${name}</span>
                    </div>
                    <button onclick="deleteAlert(${id})" class="text-gray-500 hover:text-red-400 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                    </button>
                </div>
                <div class="space-y-2">
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-400">Target ${condition}</span>
                        <span class="text-white font-bold text-emerald-400">$${targetPrice.toLocaleString()}</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-400">Current Price</span>
                        <span class="text-white">$${currentPrice.toLocaleString()}</span>
                    </div>
                </div>
                ${isTriggered ? `
                <div class="mt-4 pt-4 border-t border-red-500/20 text-center">
                    <span class="text-xs font-bold text-red-400 uppercase tracking-widest animate-pulse">⚠️ Condition Met</span>
                </div>
                ` : ''}
            `;
            container.appendChild(card);
        });
    } catch (err) {
        console.error(err);
    }
}

async function deleteAlert(id) {
    if (!confirm('Delete this alert?')) return;
    try {
        const res = await fetch(`/api/alerts/delete/${id}`, { method: 'POST' });
        if (res.ok) fetchAlerts();
    } catch (err) {
        console.error(err);
    }
}

async function populateCoinSelect() {
    try {
        const res = await fetch("/coins");
        const data = await res.json();
        const select = document.getElementById('coin_id');
        const alertSelect = document.getElementById('alert_coin_id');

        const fragment = document.createDocumentFragment();
        data.forEach(coin => {
            const option = document.createElement('option');
            option.value = coin[0]; // id
            option.textContent = `${coin[1]} - ${coin[2]}`; // symbol - name
            fragment.appendChild(option);
        });

        select.appendChild(fragment.cloneNode(true));
        if (alertSelect) alertSelect.appendChild(fragment);
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

function openAlertModal() {
    document.getElementById('alertModal').classList.remove('hidden');
}

function closeAlertModal() {
    document.getElementById('alertModal').classList.add('hidden');
}
