/* ===== Azuria REM — 2026 + Magic UI Effects ===== */

(() => {
  'use strict';

  /* --------------------------------------------------
     Blur-Fade Reveal (Magic UI blur-fade)
  -------------------------------------------------- */
  const initBlurFade = () => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
    document.querySelectorAll('.blur-fade').forEach(el => observer.observe(el));
  };

  /* --------------------------------------------------
     Light-Drawing Canvas — artisan village
     Draws houses made of glowing thin light lines,
     loops infinitely with fade between cycles.
  -------------------------------------------------- */
  const initLightDraw = () => {
    const canvas = document.getElementById('lightdraw-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width, height, dpr;

    const resize = () => {
      dpr = window.devicePixelRatio || 1;
      const rect = canvas.parentElement.getBoundingClientRect();
      width = rect.width; height = rect.height;
      canvas.width = width * dpr; canvas.height = height * dpr;
      canvas.style.width = width + 'px'; canvas.style.height = height + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    // Village artisan — flat-roof workshop buildings, no chimneys, no church
    const village = [
      // Ground
      [[.0,.72],[1,.72]],
      // Workshop 1 — small, flat roof
      [[.02,.72],[.02,.50],[.14,.50],[.14,.72]],
      // Roller door
      [[.05,.72],[.05,.58],[.11,.58],[.11,.72]],
      // Window
      [[.06,.56],[.06,.52],[.10,.52],[.10,.56]],

      // Workshop 2 — wider, slight slope
      [[.18,.72],[.18,.46],[.34,.44],[.34,.72]],
      // Two doors
      [[.20,.72],[.20,.56],[.25,.56],[.25,.72]],
      [[.27,.72],[.27,.56],[.32,.56],[.32,.72]],
      // Windows above
      [[.21,.52],[.21,.48],[.24,.48],[.24,.52]],
      [[.28,.52],[.28,.48],[.31,.48],[.31,.52]],

      // Tree 1
      [[.37,.72],[.37,.58]],[[.35,.62],[.37,.55],[.39,.62]],[[.34,.66],[.37,.58],[.40,.66]],

      // Workshop 3 — large center building, flat roof
      [[.43,.72],[.43,.42],[.63,.42],[.63,.72]],
      // Big roller door
      [[.47,.72],[.47,.52],[.59,.52],[.59,.72]],
      // Signage area
      [[.48,.48],[.58,.48],[.58,.44],[.48,.44],[.48,.48]],
      // Small windows on sides
      [[.44,.52],[.44,.48],[.46,.48],[.46,.52]],
      [[.60,.52],[.60,.48],[.62,.48],[.62,.52]],

      // Tree 2
      [[.66,.72],[.66,.58]],[[.64,.62],[.66,.55],[.68,.62]],[[.63,.66],[.66,.58],[.69,.66]],

      // Workshop 4 — medium, flat
      [[.72,.72],[.72,.48],[.86,.48],[.86,.72]],
      // Door
      [[.75,.72],[.75,.58],[.80,.58],[.80,.72]],
      // Window
      [[.81,.58],[.81,.52],[.84,.52],[.84,.58]],
      // Small vent on roof
      [[.77,.48],[.77,.45],[.81,.45],[.81,.48]],

      // Workshop 5 — small shed right
      [[.90,.72],[.90,.54],[.99,.54],[.99,.72]],
      // Door
      [[.92,.72],[.92,.60],[.97,.60],[.97,.72]],

      // Path / access road
      [[.14,.72],[.18,.76],[.34,.76],[.43,.72]],
      [[.63,.72],[.72,.76],[.86,.76],[.90,.72]],

      // Fence posts between buildings
      [[.15,.72],[.15,.67]],[[.16,.72],[.16,.67]],[[.17,.72],[.17,.67]],
      [[.15,.67],[.17,.67]],
      [[.87,.72],[.87,.67]],[[.88,.72],[.88,.67]],[[.89,.72],[.89,.67]],
      [[.87,.67],[.89,.67]],
    ];

    let progress = 0;
    const DRAW_SPEED = 0.08;
    let globalAlpha = 1;
    let lastTime = performance.now();

    const totalSegments = (drawing) => {
      let total = 0;
      for (const line of drawing) total += line.length - 1;
      return total;
    };

    const drawFrame = (time) => {
      const dt = Math.min((time - lastTime) / 1000, 0.05);
      lastTime = time;
      progress += dt * DRAW_SPEED;

      if (progress < 1) {
        globalAlpha = 1;
      } else if (progress < 1.4) {
        globalAlpha = 1;
      } else if (progress < 1.9) {
        globalAlpha = 1 - (progress - 1.4) / 0.5;
      } else if (progress < 2.2) {
        globalAlpha = 0;
      } else {
        progress = 0;
        globalAlpha = 0;
      }

      ctx.clearRect(0, 0, width, height);
      if (globalAlpha <= 0) { requestAnimationFrame(drawFrame); return; }

      const drawing = village;
      const total = totalSegments(drawing);
      const segsToDraw = Math.floor(Math.min(progress, 1) * total);
      const segFrac = (Math.min(progress, 1) * total) - segsToDraw;

      let segCount = 0;
      // Full-canvas drawing — use full width/height with padding
      const padX = width * 0.03, padY = height * 0.08;
      const drawW = width - padX * 2, drawH = height - padY * 2;

      for (const line of drawing) {
        for (let i = 0; i < line.length - 1; i++) {
          if (segCount > segsToDraw) break;
          const [x1, y1] = line[i];
          const [x2, y2] = line[i + 1];
          const px1 = padX + x1 * drawW, py1 = padY + y1 * drawH;
          const px2 = padX + x2 * drawW, py2 = padY + y2 * drawH;

          let endX = px2, endY = py2;
          if (segCount === segsToDraw) {
            endX = px1 + (px2 - px1) * segFrac;
            endY = py1 + (py2 - py1) * segFrac;
          }

          // Soft glow
          ctx.save();
          ctx.globalAlpha = globalAlpha * 0.15;
          ctx.strokeStyle = '#faf8f5';
          ctx.lineWidth = 4;
          ctx.lineCap = 'round';
          ctx.shadowColor = 'rgba(250,248,245,0.4)';
          ctx.shadowBlur = 12;
          ctx.beginPath();
          ctx.moveTo(px1, py1);
          ctx.lineTo(endX, endY);
          ctx.stroke();
          ctx.restore();

          // Thin core
          ctx.save();
          ctx.globalAlpha = globalAlpha * 0.5;
          ctx.strokeStyle = 'rgba(250,248,245,0.8)';
          ctx.lineWidth = 0.8;
          ctx.lineCap = 'round';
          ctx.shadowColor = 'rgba(250,248,245,0.3)';
          ctx.shadowBlur = 4;
          ctx.beginPath();
          ctx.moveTo(px1, py1);
          ctx.lineTo(endX, endY);
          ctx.stroke();
          ctx.restore();

          // Bright dot at drawing tip
          if (segCount === segsToDraw) {
            ctx.save();
            ctx.globalAlpha = globalAlpha * 0.8;
            ctx.fillStyle = '#fff';
            ctx.shadowColor = 'rgba(255,255,255,0.6)';
            ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.arc(endX, endY, 1.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
          }

          segCount++;
        }
        if (segCount > segsToDraw) break;
      }

      requestAnimationFrame(drawFrame);
    };

    resize();
    requestAnimationFrame(drawFrame);
    window.addEventListener('resize', resize);
  };

  /* --------------------------------------------------
     Particles Canvas (Magic UI particles)
  -------------------------------------------------- */
  const initParticles = () => {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width, height, particles, mouse = { x: 0, y: 0 };

    const resize = () => {
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.parentElement.getBoundingClientRect();
      width = rect.width; height = rect.height;
      canvas.width = width * dpr; canvas.height = height * dpr;
      canvas.style.width = width + 'px'; canvas.style.height = height + 'px';
      ctx.scale(dpr, dpr);
    };

    const createParticles = () => {
      const count = Math.min(Math.floor((width * height) / 8000), 120);
      particles = [];
      for (let i = 0; i < count; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          size: Math.random() * 1.8 + 0.4,
          alpha: Math.random() * 0.5 + 0.1,
          targetAlpha: Math.random() * 0.5 + 0.1,
          dx: (Math.random() - 0.5) * 0.3,
          dy: (Math.random() - 0.5) * 0.3,
          magnetism: Math.random() * 0.5 + 0.5,
          translateX: 0, translateY: 0,
        });
      }
    };

    const draw = () => {
      ctx.clearRect(0, 0, width, height);
      for (const p of particles) {
        p.x += p.dx; p.y += p.dy;
        if (p.x < 0) p.x = width; if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height; if (p.y > height) p.y = 0;
        const mx = mouse.x - p.x, my = mouse.y - p.y;
        const dist = Math.sqrt(mx * mx + my * my);
        if (dist < 200) {
          const force = (200 - dist) / 200;
          p.translateX += (mx * force * p.magnetism - p.translateX) * 0.05;
          p.translateY += (my * force * p.magnetism - p.translateY) * 0.05;
        } else {
          p.translateX *= 0.95; p.translateY *= 0.95;
        }
        p.alpha += (p.targetAlpha - p.alpha) * 0.05;
        if (Math.random() < 0.005) p.targetAlpha = Math.random() * 0.5 + 0.1;
        ctx.beginPath();
        ctx.arc(p.x + p.translateX, p.y + p.translateY, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(250,248,245,${p.alpha})`;
        ctx.fill();
      }
      requestAnimationFrame(draw);
    };

    const handleMouse = (e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    };

    resize(); createParticles(); draw();
    window.addEventListener('resize', () => { resize(); createParticles(); });
    window.addEventListener('mousemove', handleMouse, { passive: true });
  };

  /* --------------------------------------------------
     Flickering Grid Canvas (Magic UI flickering-grid)
  -------------------------------------------------- */
  const initFlickeringGrid = () => {
    document.querySelectorAll('.flickering-grid-wrap').forEach(wrap => {
      const canvas = wrap.querySelector('canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const squareSize = 3, gridGap = 5, maxOpacity = 0.25;
      const flickerChance = 0.15;
      const color = wrap.dataset.color || '250,248,245';
      let width, height, cols, rows, squares, dpr, lastTime = 0;

      const setup = () => {
        dpr = window.devicePixelRatio || 1;
        const rect = wrap.getBoundingClientRect();
        width = rect.width; height = rect.height;
        canvas.width = width * dpr; canvas.height = height * dpr;
        canvas.style.width = width + 'px'; canvas.style.height = height + 'px';
        cols = Math.floor(width / (squareSize + gridGap));
        rows = Math.floor(height / (squareSize + gridGap));
        squares = new Float32Array(cols * rows);
        for (let i = 0; i < squares.length; i++) squares[i] = Math.random() * maxOpacity;
      };

      const draw = (time) => {
        const dt = Math.min((time - lastTime) / 1000, 0.1); lastTime = time;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < cols; i++) {
          for (let j = 0; j < rows; j++) {
            const idx = i * rows + j;
            if (Math.random() < flickerChance * dt) squares[idx] = Math.random() * maxOpacity;
            ctx.fillStyle = `rgba(${color},${squares[idx]})`;
            ctx.fillRect(
              i * (squareSize + gridGap) * dpr,
              j * (squareSize + gridGap) * dpr,
              squareSize * dpr, squareSize * dpr
            );
          }
        }
        requestAnimationFrame(draw);
      };

      setup();
      requestAnimationFrame(draw);
      window.addEventListener('resize', setup);
    });
  };

  /* --------------------------------------------------
     Navbar
  -------------------------------------------------- */
  const initNav = () => {
    const nav = document.querySelector('.navbar');
    if (!nav) return;
    let ticking = false;
    const onScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          nav.classList.toggle('scrolled', window.scrollY > 60);
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  };

  /* --------------------------------------------------
     Mobile menu
  -------------------------------------------------- */
  const initMenu = () => {
    const btn = document.querySelector('.hamburger');
    const links = document.querySelector('.navbar__links');
    if (!btn || !links) return;
    const toggle = () => {
      btn.classList.toggle('open');
      links.classList.toggle('open');
      document.body.style.overflow = links.classList.contains('open') ? 'hidden' : '';
    };
    btn.addEventListener('click', toggle);
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      if (links.classList.contains('open')) toggle();
    }));
  };

  /* --------------------------------------------------
     Active nav link
  -------------------------------------------------- */
  const initActiveLink = () => {
    const current = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.navbar__links a').forEach(a => {
      if (a.getAttribute('href') === current) a.classList.add('active');
    });
  };

  /* Contact form is handled inline on contact.html */
  const initForm = () => {};

  /* --------------------------------------------------
     Login Modal + Role-Based Access
  -------------------------------------------------- */
  const ACCOUNTS = {
    mnc: { hash: '4e457638342d466278713957664f6e2d646b49455451', role: 'admin' }
  };

  // Simple hex encode/decode for obfuscation (not crypto-secure, just not plaintext)
  const _h2s = h => { let s = ''; for (let i = 0; i < h.length; i += 2) s += String.fromCharCode(parseInt(h.substr(i, 2), 16)); return s; };

  const initLoginModal = () => {
    const overlay = document.getElementById('login-overlay');
    if (!overlay) return;
    const close = overlay.querySelector('.login-modal__close');
    const form = overlay.querySelector('form');

    // Check if already logged in — only auto-act on Espace Partenaires click, not page load
    // (so admins can browse normal pages without being redirected to scanner)

    // Open
    document.querySelectorAll('.nav-login').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const session = sessionStorage.getItem('azuria_session');
        if (session) {
          try {
            const s = JSON.parse(session);
            if (s.role === 'admin') { _showAdminPanel(); return; }
            if (s.role === 'partenaire') { _showPartnerPanel(); return; }
          } catch(e) {}
        }
        overlay.style.display = 'flex';
        requestAnimationFrame(() => overlay.classList.add('open'));
      });
    });

    // Close
    const closeModal = () => {
      overlay.classList.remove('open');
      setTimeout(() => overlay.style.display = 'none', 300);
    };
    if (close) close.addEventListener('click', closeModal);
    overlay.addEventListener('click', (e) => { if (e.target === overlay) closeModal(); });

    // Submit
    if (form) form.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = form.querySelector('#login-email').value.trim().toLowerCase();
      const pass = form.querySelector('#login-pass').value;
      const btn = form.querySelector('button');
      btn.textContent = 'Vérification...';
      btn.disabled = true;

      setTimeout(() => {
        const account = ACCOUNTS[email];
        if (account && pass === _h2s(account.hash)) {
          sessionStorage.setItem('azuria_session', JSON.stringify({ user: email, role: account.role }));
          closeModal();
          btn.textContent = 'Se connecter';
          btn.disabled = false;
          if (account.role === 'admin') _showAdminPanel();
          else _showPartnerPanel();
        } else {
          btn.textContent = 'Identifiants non reconnus';
          btn.style.background = '#6b1a1b';
          setTimeout(() => {
            btn.textContent = 'Se connecter';
            btn.style.background = '';
            btn.disabled = false;
          }, 2000);
        }
      }, 800);
    });
  };

  const _showAdminPanel = () => {
    // Navigate to scanner page if not already there
    const current = window.location.pathname.split('/').pop() || 'index.html';
    if (current !== 'scanner.html') {
      window.location.href = 'scanner.html';
    }
  };

  const _showPartnerPanel = () => {
    // Future: navigate to partner dashboard
    // For now show a message
    const overlay = document.getElementById('login-overlay');
    if (overlay) {
      const modal = overlay.querySelector('.login-modal');
      if (modal) {
        modal.innerHTML = `
          <button class="login-modal__close" onclick="this.closest('.login-overlay').classList.remove('open');setTimeout(()=>this.closest('.login-overlay').style.display='none',300)">&times;</button>
          <h3>Espace Partenaires</h3>
          <p style="margin:1.5rem 0;color:var(--silver-dim)">Votre espace partenaire est en cours de construction.<br>Nous vous informerons dès qu'il sera disponible.</p>
          <button class="login-modal__btn" onclick="sessionStorage.removeItem('azuria_session');window.location.reload()">Se déconnecter</button>
        `;
      }
      overlay.style.display = 'flex';
      requestAnimationFrame(() => overlay.classList.add('open'));
    }
  };

  /* --------------------------------------------------
     Init
  -------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', () => {
    initBlurFade();
    initLightDraw();
    initParticles();
    initFlickeringGrid();
    initNav();
    initMenu();
    initActiveLink();
    initForm();
    initLoginModal();
  });
})();
