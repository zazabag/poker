const API_URL = 'http://localhost:8000';
let currentUser = null;
let tg = window.Telegram?.WebApp;

if (tg) {
    tg.expand();
    tg.ready();
    if (tg.initDataUnsafe?.user?.id) {
        currentUser = tg.initDataUnsafe.user;
    }
}

// Navigation
const navBtns = document.querySelectorAll('.nav-btn');
const pages = document.querySelectorAll('.page');

navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const pageId = btn.dataset.page;
        navBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        pages.forEach(p => p.classList.remove('active'));
        document.getElementById(`page-${pageId}`).classList.add('active');
        if (pageId === 'tournaments') loadTournaments();
        if (pageId === 'leaderboard') loadLeaderboard();
        if (pageId === 'profile') loadProfile();
    });
});

// API Helpers
async function apiGet(path) {
    const res = await fetch(`${API_URL}${path}`);
    if (!res.ok) throw new Error('API Error');
    return res.json();
}

async function apiPost(path, body) {
    const res = await fetch(`${API_URL}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    if (!res.ok) throw new Error('API Error');
    return res.json();
}

// Home Page
async function loadHome() {
    try {
        const tournaments = await apiGet('/tournaments');
        const upcoming = tournaments.filter(t => t.status === 'open');
        
        if (upcoming.length > 0) {
            const next = upcoming[0];
            document.getElementById('next-tournament-title').textContent = next.title;
            document.getElementById('next-tournament-date').textContent = next.date;
            document.getElementById('next-tournament-time').textContent = next.time;
            
            const count = next.registered_count || 0;
            const max = next.max_players;
            document.getElementById('seats-info').textContent = `Мест: ${count} / ${max}`;
            document.getElementById('seats-fill').style.width = `${(count / max) * 100}%`;
            
            const btn = document.getElementById('btn-register-main');
            if (count >= max) {
                btn.textContent = 'SOLD OUT';
                btn.disabled = true;
                btn.style.opacity = '0.5';
            } else {
                btn.textContent = 'Записаться';
                btn.disabled = false;
                btn.style.opacity = '1';
                btn.onclick = () => registerForTournament(next.id);
            }
        } else {
            document.getElementById('next-tournament-title').textContent = 'Нет ближайших турниров';
            document.getElementById('btn-register-main').style.display = 'none';
        }
    } catch (e) {
        console.error(e);
        document.getElementById('next-tournament-title').textContent = 'Ошибка загрузки';
    }
}

// Tournaments Page
async function loadTournaments() {
    const list = document.getElementById('tournaments-list');
    list.innerHTML = '<div class="loading">Загрузка...</div>';
    
    try {
        const tournaments = await apiGet('/tournaments');
        if (!tournaments.length) {
            list.innerHTML = '<div class="empty">Пока нет турниров</div>';
            return;
        }
        
        list.innerHTML = tournaments.map(t => {
            const count = t.registered_count || 0;
            const max = t.max_players;
            const isFull = count >= max;
            const statusClass = isFull ? 'status-full' : (t.status === 'open' ? 'status-open' : 'status-closed');
            const statusText = isFull ? 'SOLD OUT' : (t.status === 'open' ? 'Запись открыта' : 'Закрыт');
            
            return `
                <div class="tournament-card">
                    <div class="tournament-title">${t.title}</div>
                    <div class="tournament-meta">
                        <span class="gold">📅 ${t.date}</span>
                        <span>🕐 ${t.time}</span>
                        <span>👥 ${count}/${max}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                        <span class="tournament-status ${statusClass}">${statusText}</span>
                        ${t.status === 'open' && !isFull ? `<button class="btn-small" onclick="registerForTournament(${t.id})">Записаться</button>` : ''}
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        list.innerHTML = '<div class="empty">Ошибка загрузки</div>';
    }
}

// Leaderboard
async function loadLeaderboard() {
    const list = document.getElementById('leaderboard-list');
    list.innerHTML = '<div class="loading">Загрузка...</div>';
    
    try {
        const data = await apiGet('/leaderboard');
        if (!data.length) {
            list.innerHTML = '<div class="empty">Пока нет данных</div>';
            return;
        }
        
        list.innerHTML = data.map((player, i) => {
            const placeClass = i === 0 ? 'place-1' : (i === 1 ? 'place-2' : (i === 2 ? 'place-3' : 'place-other'));
            return `
                <div class="lb-row">
                    <div class="lb-place ${placeClass}">${i + 1}</div>
                    <div class="lb-info">
                        <div class="lb-name">${player.nickname}</div>
                        <div class="lb-stats">${player.games} игр | ${player.wins} 🏆 | ${player.finals} 🥉</div>
                    </div>
                    <div class="lb-points">${player.total_points}</div>
                </div>
            `;
        }).join('');
    } catch (e) {
        list.innerHTML = '<div class="empty">Ошибка загрузки</div>';
    }
}

// Profile
async function loadProfile() {
    if (!currentUser) {
        document.getElementById('profile-name').textContent = 'Гость';
        document.getElementById('profile-id').textContent = 'Войдите через Telegram';
        return;
    }
    
    try {
        // Get or create user
        let user;
        try {
            user = await apiGet(`/users/${currentUser.id}`);
        } catch (e) {
            // Create user
            await apiPost('/users', {
                telegram_id: currentUser.id,
                username: currentUser.username || currentUser.first_name,
                nickname: currentUser.username || currentUser.first_name
            });
            user = await apiGet(`/users/${currentUser.id}`);
        }
        
        document.getElementById('profile-name').textContent = user.nickname;
        document.getElementById('profile-id').textContent = `ID: ${user.id}`;
        
        const stats = await apiGet(`/users/${user.id}/stats`);
        if (stats.stats) {
            document.getElementById('stat-games').textContent = stats.stats.games || 0;
            document.getElementById('stat-points').textContent = stats.stats.total_points || 0;
            document.getElementById('stat-wins').textContent = stats.stats.wins || 0;
            document.getElementById('stat-finals').textContent = stats.stats.finals || 0;
        }
        
        const historyEl = document.getElementById('history-list');
        if (stats.history && stats.history.length) {
            historyEl.innerHTML = stats.history.map(h => `
                <div class="history-item">
                    <div>
                        <div class="history-tournament">${h.title}</div>
                        <div class="history-date">${h.date}</div>
                    </div>
                    <div class="history-place">${h.place} место</div>
                </div>
            `).join('');
        } else {
            historyEl.innerHTML = '<div class="empty">Пока нет истории</div>';
        }
    } catch (e) {
        console.error(e);
    }
}

// Register
async function registerForTournament(tournamentId) {
    if (!currentUser) {
        alert('Откройте приложение через Telegram бота для записи');
        return;
    }
    
    try {
        let user = await apiGet(`/users/${currentUser.id}`);
        await apiPost('/register', { tournament_id: tournamentId, user_id: user.id });
        alert('✅ Вы записаны!');
        loadHome();
        loadTournaments();
    } catch (e) {
        alert('❌ Ошибка: возможно, вы уже записаны или мест нет');
    }
}

// Init
loadHome();
