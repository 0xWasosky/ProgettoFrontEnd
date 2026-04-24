<script>
export default {
  data() {
    return {
      imgLoaded: false,
      progress: 0,
      imgSrc: "https://picsum.photos/400",
      interval: null,
      resetTimeout: null
    };
  },

  mounted() {
    this.startDownload();
  },

  beforeUnmount() {
    clearInterval(this.interval);
    clearTimeout(this.resetTimeout);
  },

  methods: {
    startDownload() {
      this.progress = 0;
      this.imgLoaded = false;

      this.interval = setInterval(() => {
        if (this.progress < 100) {
          this.progress += 4;
        } else {
          clearInterval(this.interval);

          this.imgLoaded = true;

          if (this.$refs.text) {
            this.$refs.text.textContent = "Download completato";
          }

          if (this.$refs.glow) {
            this.$refs.glow.classList.add("active");
          }

          this.resetTimeout = setTimeout(() => {
            if (this.$refs.glow) {
              this.$refs.glow.classList.remove("active");
            }
            this.startDownload();
          }, 2000);
        }
      }, 120);
    }
  }
};
</script>

<template>
  <div class="wrapper">

    <nav>
      <div id="accountIcon">
        <router-link to="/home">
          <img src="../../assets/images/home.png" width="100%"/>
        </router-link>
      </div>
    </nav>

    <div class="content">
      <div class="phone">
        <div class="screen">

          <div class="notch"></div>

          <div class="top-info">
            Download Manager
            <span>Scaricamento file in corso</span>
          </div>

          <img v-if="imgLoaded" :src="imgSrc" class="image" />

          <div v-else class="loader">
            <div class="bar">
              <div class="fill" :style="{ width: progress + '%' }"></div>
            </div>

            <div class="percent">{{ progress }}%</div>
          </div>

          <div class="glow" ref="glow"></div>

          <div class="text" ref="text">
            Download in corso...
          </div>

        </div>
      </div>

      <div class="info">
        <h2>Download System</h2>

        <p>
          Scarica le foto di classe delle altre classi in modo rapido e automatico.
        </p>

        <ol>
          <li>Visualizza tutte le foto disponibili</li>
          <li>Seleziona la tua classe</li>
          <li>Scarica e condividi i contenuti</li>
        </ol>

        <p class="hint">
          Interfaccia demo con download in loop automatico.
        </p>
      </div>

    </div>

    <!-- NEXT -->
    <router-link to="/classes" class="next-btn">
      Visualizza Classi →
    </router-link>

  </div>
</template>

<style src="../stylesheets/defaultStyle.css"></style>

<style scoped>

.wrapper{
  min-height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  padding:20px;
  background:#1a1a1a;
  font-family:sans-serif;
  position:relative;
  box-sizing:border-box;
}

.nav{
  position:absolute;
  top:10px;
  left:10px;
  width:40px;
}

.nav img{
  width:100%;
}

.content{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:80px;
  flex-wrap:wrap;
  width:100%;
  max-width:1100px;
}

.phone{
  width:260px;
  aspect-ratio: 1 / 2;
  background:#000;
  border-radius:40px;
  padding:15px;
  box-shadow:0 20px 60px rgba(0,0,0,0.8);
}

.screen{
  width:100%;
  height:100%;
  background:#111;
  border-radius:30px;
  position:relative;
  overflow:hidden;

  display:flex;
  justify-content:center;
  align-items:center;
  flex-direction:column;
}

.notch{
  position:absolute;
  top:10px;
  width:120px;
  height:18px;
  background:#000;
  border-radius:10px;
}

.top-info{
  position:absolute;
  top:40px;
  width:100%;
  text-align:center;
  color:#00ffc3;
  font-size:13px;
}

.top-info span{
  display:block;
  font-size:11px;
  opacity:0.7;
}

.image{
  width:65%;
  max-width:200px;
  border-radius:12px;
  box-shadow:0 0 25px rgba(0,255,195,0.2);
  animation:fadeIn 0.5s ease;
}

@keyframes fadeIn{
  from{opacity:0; transform:scale(0.95);}
  to{opacity:1; transform:scale(1);}
}

.loader{
  width:75%;
  text-align:center;
}

.bar{
  width:100%;
  height:6px;
  background:#333;
  border-radius:10px;
  overflow:hidden;
  margin-bottom:10px;
}

.fill{
  height:100%;
  background:#00ffc3;
  transition:0.2s;
}

.percent{
  color:#00ffc3;
  font-size:14px;
}

.text{
  position:absolute;
  bottom:18px;
  width:100%;
  text-align:center;
  color:#00ffc3;
  font-size:13px;
}

.glow{
  position:absolute;
  width:100%;
  height:100%;
  background:rgba(0,255,195,0.15);
  opacity:0;
}

.glow.active{
  animation:flash 0.6s;
}

@keyframes flash{
  0%{opacity:0}
  50%{opacity:1}
  100%{opacity:0}
}

.info{
  max-width:360px;
  width:100%;
  color:#fff;
}

.info h2{
  color:#00ffc3;
  margin-bottom:10px;
}

.info p{
  opacity:0.8;
  line-height:1.5;
}

.info ol{
  margin:15px 0;
  padding-left:20px;
}

.info li{
  margin-bottom:8px;
}

.hint{
  margin-top:15px;
  font-size:13px;
  color:#00ffc3;
}

.next-btn{
  position:fixed;
  bottom:20px;
  right:20px;

  padding:10px 18px;
  background:#00ffc3;
  color:#000;
  font-weight:600;
  text-decoration:none;
  border-radius:12px;
  box-shadow:0 0 15px rgba(0,255,195,0.4);
  transition:0.25s ease;
}

.next-btn:hover{
  transform:translateY(-3px);
}

.next-btn:active{
  transform:scale(0.95);
}


@media (max-width: 768px){

  .content{
    flex-direction:column;
    gap:30px;
  }

  .info{
    text-align:center;
  }

  .phone{
    width:220px;
  }

  .next-btn{
    bottom:15px;
    right:15px;
    font-size:14px;
    padding:8px 14px;
  }
}
</style>