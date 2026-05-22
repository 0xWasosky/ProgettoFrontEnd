<script setup>
import { ref, onMounted } from 'vue'

const isDarkMode = ref(false)

const applyTheme = (theme) => {
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
  isDarkMode.value = theme === 'dark'
}

const toggleTheme = () => {
  applyTheme(isDarkMode.value ? 'light' : 'dark')
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme') || 'light'
  applyTheme(savedTheme)
})
</script>

<template>

  <nav aria-label="Navigazione principale" class="top-nav" style="min-width: fit-content;">
    <router-link to="/">Torna alla home</router-link>
  </nav>

  <button
    type="button"
    class="theme-toggle"
    @click="toggleTheme"
    :aria-pressed="isDarkMode"
    aria-label="Cambia tema"
  >
    {{ isDarkMode ? '☼' : '☀︎' }}
  </button>

  <main class="about-page">
    <section class="hero" aria-labelledby="titolo-annuario">
      <div class="hero-copy">
        <span class="eyebrow">Annuario</span>
        <h1 id="titolo-annuario">Annuario Digitale della Scuola</h1>
        <p class="hero-text">
          In questa piattaforma vengono raccolti file audio registrati dagli 
          studenti della scuola nel quale raccontano: come hanno passato il loro
          anno scolastico, cosa hanno fatto, le cose che hanno imparato, le gite che hanno fatto etc..
          <br><br>
          Verranno inoltre caricate le foto di classe di ciascuna classe; non appena disponibili, sarà possibile scaricarle.
        </p>

        <div class="hero-actions">
          <router-link to="/login" class="cta-primary">Vai al login</router-link>
          <!--<a href="#funzionalita" class="cta-secondary">Scopri le funzioni</a>-->
        </div>
      </div>

      <aside class="hero-panel" aria-label="Punti chiave del progetto">
        <div class="mini-card">
          <strong>Audio</strong>
          <span>Ogni studente puo raccontare come ha vissuto il proprio anno scolastico</span>
        </div>
        <div class="mini-card">
          <strong>QR code</strong>
          <span>Una volta caricato l'audio verrà generato un QR code e sarà possibile scaricare l'<audio src=""></audio></span>
        </div>
        <div class="mini-card">
          <strong>Classe</strong>
          <span>Le fotografie sono organizzate e restano accessibili</span>
        </div>
      </aside>
    </section>

    <section class="section intro" aria-labelledby="descrizione-progetto">
      <div>
        <span class="section-label">Descrizione</span>
        <h2 id="descrizione-progetto">Un annuario scolastico</h2>
      </div>
      <p>
        Questo annuario digitale permette agli studenti di condividere contenuti
        personali, esplorare classi e profili, e custodire i momenti piu
        significativi dell'esperienza scolastica da qualsiasi dispositivo.
      </p>
    </section>

    <section class="section" id="funzionalita" aria-labelledby="funzionalita-title">
      <div class="section-heading">
        <span class="section-label">Funzionalità</span>
        <h2 id="funzionalita-title">Dovrebbe servire a condividere la propria esperienza sull'anno scolastico</h2>
      </div>

      <div class="features-grid">
        <article class="feature-card">
          <span class="feature-icon">01</span>
          <h3>Audio degli studenti</h3>
          <p>
            Ogni studente puo caricare un messaggio vocale personale per
            raccontare il proprio anno, le esperienze vissute e il legame con la
            classe.
          </p>
          <small>
            La responsabilità dei contenuti pubblicati nei file audio resta
            dell'utente.
          </small>
        </article>

        <article class="feature-card">
          <span class="feature-icon">02</span>
          <h3>QR code per ogni audio</h3>
          <p>
            Ogni registrazione viene associata a un QR code così da poter essere
            aperta o scaricata velocemente anche da smartphone.
          </p>
        </article>

        <article class="feature-card">
          <span class="feature-icon">03</span>
          <h3>Elenco classi e studenti</h3>
          <p>
            La piattaforma raccoglie l'intero elenco delle classi della scuola e
            rende più semplice ritrovare studenti, profili e materiali.
          </p>
        </article>

        <article class="feature-card">
          <span class="feature-icon">04</span>
          <h3>Foto di classe</h3>
          <p>
            Le foto di classe possono essere visualizzate e scaricate.
          </p>
        </article>
      </div>
    </section>

    <section class="section workflow" aria-labelledby="come-funziona">
      <div class="section-heading">
        <span class="section-label">Percorso</span>
        <h2 id="come-funziona">Come funziona</h2>
      </div>

      <ol class="steps" type="1">
        <li>
          <strong>Accedere al profilo</strong>
          <span>Entrare nell'area personale per iniziare a partecipare all'annuario.</span>
        </li>
        <li>
          <strong>Caricacare un audio</strong>
          <span>Registrare o invia un messaggio che racconti il tuo anno scolastico.</span>
        </li>
        <li>
          <strong>Condividere tramite QR code</strong>
          <span>Il sistema genera un QR code visibile e scaricabile da tutti.</span>
        </li>
        <li>
          <strong>Esplorare e conservare le fotografie e gli audio</strong>
          <span>Quando disponibili, si potranno visualizzare e scaricare anche le foto di classe.</span>
        </li>
      </ol>
    </section>
  </main>
</template>

<style src="../stylesheets/defaultStyle.css"></style>

<style scoped>
.about-page {
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto;
  padding: 7rem 0 3rem;
}

.hero,
.section {
  background: linear-gradient(145deg, color-mix(in srgb, var(--card-bg) 92%, white 8%), var(--card-bg));
  border: 1px solid color-mix(in srgb, var(--borders) 22%, transparent);
  border-radius: 28px;
  box-shadow: 0 22px 60px rgba(0, 0, 0, 0.08);
}

.hero {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 2rem;
  padding: clamp(2rem, 5vw, 4rem);
  margin-bottom: 1.75rem;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: "";
  position: absolute;
  inset: auto -10% -35% auto;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle, color-mix(in srgb, var(--button-bg) 30%, transparent), transparent 68%);
  pointer-events: none;
}

.eyebrow,
.section-label {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--button-bg);
  font-weight: 700;
}

.hero h1 {
  margin: 0.75rem 0 1rem;
  font-size: clamp(2.4rem, 5vw, 4.5rem);
  line-height: 0.98;
  color: var(--text-color);
}

.hero-text {
  max-width: 60ch;
  font-size: 1.08rem;
  line-height: 1.7;
  color: color-mix(in srgb, var(--text-color) 84%, transparent);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.9rem;
  margin-top: 1.75rem;
}

.cta-primary,
.cta-secondary {
  text-decoration: none;
  border-radius: 999px;
  padding: 0.95rem 1.35rem;
  font-weight: 700;
  transition: transform 0.25s ease, background 0.25s ease, color 0.25s ease;
}

.cta-primary {
  background: var(--button-bg);
  color: white;
}

.cta-secondary {
  border: 1px solid color-mix(in srgb, var(--borders) 35%, transparent);
  color: var(--text-color);
  background: color-mix(in srgb, var(--card-bg) 88%, transparent);
}

.cta-primary:hover,
.cta-secondary:hover {
  transform: translateY(-2px);
}

.hero-panel {
  display: grid;
  gap: 1rem;
  align-content: center;
}

.mini-card {
  display: grid;
  gap: 0.45rem;
  padding: 1.15rem;
  border-radius: 20px;
  background: color-mix(in srgb, var(--bg-color) 55%, var(--card-bg));
  border: 1px solid color-mix(in srgb, var(--borders) 18%, transparent);
}

.mini-card strong {
  color: var(--text-color);
  font-size: 1rem;
}

.mini-card span,
.section p,
.feature-card p,
.feature-card small,
.steps span {
  line-height: 1.65;
  color: color-mix(in srgb, var(--text-color) 82%, transparent);
}

.section {
  padding: clamp(1.5rem, 4vw, 2.4rem);
  margin-bottom: 1.5rem;
}

.intro {
  display: grid;
  grid-template-columns: 0.95fr 1.25fr;
  gap: 1.5rem;
  align-items: center;
}

.section-heading h2,
.intro h2 {
  margin: 0.55rem 0 0;
  font-size: clamp(1.6rem, 3vw, 2.3rem);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.feature-card {
  padding: 1.4rem;
  border-radius: 22px;
  background: color-mix(in srgb, var(--bg-color) 60%, var(--card-bg));
  border: 1px solid color-mix(in srgb, var(--borders) 16%, transparent);
}

.feature-card h3 {
  margin: 0.9rem 0 0.6rem;
  font-size: 1.15rem;
}

.feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: color-mix(in srgb, var(--button-bg) 16%, transparent);
  color: var(--button-bg);
  font-weight: 800;
}

.workflow {
  position: relative;
}

.steps {
  list-style: none;
  counter-reset: step-counter;
  padding: 0;
  margin: 1.5rem 0 0;
  display: grid;
  gap: 1rem;
}

.steps li {
  counter-increment: step-counter;
  display: grid;
  gap: 0.4rem;
  padding: 1.2rem 1.2rem 1.2rem 4.2rem;
  border-radius: 20px;
  background: color-mix(in srgb, var(--bg-color) 60%, var(--card-bg));
  border: 1px solid color-mix(in srgb, var(--borders) 16%, transparent);
  position: relative;
}

.steps li::before {
  content: counter(step-counter);
  position: absolute;
  left: 1.2rem;
  top: 1.15rem;
  width: 2rem;
  height: 2rem;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--button-bg);
  color: white;
  font-weight: 700;
}

.steps strong {
  color: var(--text-color);
  font-size: 1.02rem;
}

@media (max-width: 900px) {
  .about-page {
    padding-top: 6.5rem;
  }

  .hero,
  .intro {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .about-page {
    width: min(100% - 1rem, 1120px);
    padding-top: 5.5rem;
  }

  .hero,
  .section {
    border-radius: 22px;
  }

  .hero-actions {
    flex-direction: column;
  }

  .cta-primary,
  .cta-secondary {
    text-align: center;
    width: 100%;
  }

  .steps li {
    padding-left: 1.2rem;
    padding-top: 3.7rem;
  }

  .steps li::before {
    top: 1rem;
  }
}
</style>
