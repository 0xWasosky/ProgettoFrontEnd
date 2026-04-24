<script>
import QRCode from "qrcode";

export default {
  data() {
    return {
      qrSrc: ""
    };
  },
  mounted() {
    QRCode.toDataURL("https://sito.it", {
      width: 140,
      margin: 1
    }).then(url => {
      this.qrSrc = url;
    });

    setTimeout(() => {
      if (this.$refs.text) {
        this.$refs.text.textContent = "QR rilevato";
      }
      if (this.$refs.glow) {
        this.$refs.glow.classList.add("active");
      }
    }, 3000);
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

          <img v-if="qrSrc" :src="qrSrc" class="qr" />

          <div class="scan-box">
            <div class="line"></div>
          </div>

          <div class="glow" ref="glow"></div>

          <div class="text" ref="text">
            Scansione QR...
          </div>

        </div>
      </div>

      <div class="info">
        <h2>Scanner QR</h2>

        <p>
          Scansiona codici QR in modo rapido e sicuro direttamente dal tuo dispositivo.
        </p>

        <ul>
          <li>📷 Inquadra il codice</li>
          <li>💾 Salva file audio degli altri studenti</li>
          <li>🎤 Ascolta registrazioni condivise</li>
        </ul>

        <p class="hint">
          Troverai i QR dei file audio nella sezione classi
        </p>
      </div>

    </div>

    <router-link to="/presentation2" class="next-btn">
      Next →
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
  box-sizing:border-box;
  background:#1a1a1a;
  font-family:sans-serif;
  position:relative;
}

.content{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:60px;
  flex-wrap:wrap;
  width:100%;
  max-width:1100px;
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


.phone{
  width:260px;
  aspect-ratio: 1 / 2;
  background:#000;
  border-radius:40px;
  box-shadow:0 20px 60px rgba(0,0,0,0.8);
  padding:15px;
}

.screen{
  width:100%;
  height:100%;
  border-radius:30px;
  background:#111;
  position:relative;
  overflow:hidden;
}

.notch{
  position:absolute;
  top:8px;
  left:50%;
  transform:translateX(-50%);
  width:120px;
  height:20px;
  background:#000;
  border-radius:10px;
}

.qr{
  width:45%;
  max-width:140px;
  height:auto;
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%) rotate(8deg);
  background:#fff;
  padding:6px;
  border-radius:10px;
}

.scan-box{
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  width:170px;
  height:170px;
  border:2px solid #00ffc3;
  border-radius:15px;
  box-shadow:0 0 20px rgba(0,255,195,0.5);
}

.line{
  position:absolute;
  width:100%;
  height:3px;
  background:#00ffc3;
  animation:scan 2s linear infinite;
}

@keyframes scan{
  0%{top:0}
  100%{top:100%}
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

.text{
  position:absolute;
  bottom:15px;
  width:100%;
  text-align:center;
  color:#00ffc3;
  font-size:13px;
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

.info ul{
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
  transition:all 0.25s ease;
}

.next-btn:hover{
  transform:translateY(-3px);
  box-shadow:0 0 25px rgba(0,255,195,0.6);
}

.next-btn:active{
  transform:scale(0.95);
}

@media (max-width: 768px){

  .content{
    flex-direction:column;
    gap:25px;
  }

  .phone{
    width:220px;
  }

  .info{
    text-align:center;
  }

  .scan-box{
    width:150px;
    height:150px;
  }

  .next-btn{
    bottom:15px;
    right:15px;
    font-size:14px;
    padding:8px 14px;
  }
}

</style>