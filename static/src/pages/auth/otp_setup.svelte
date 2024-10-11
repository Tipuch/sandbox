<script>
  //  import * as QRCode from "qrcode";
  export let messages;
  export let errors;
  export let has_active_otp;

  let pyotpUri = "";
  let currentUser = null;

  async function generateTOTPSecret() {
    const response = await fetch("/auth/otp");
    const responseJson = await response.json();
    if (response.status === 200) {
      currentUser = responseJson;
      pyotpUri = currentUser.pyotp_uri;
      // QRCode.toCanvas(
      //   document.getElementById("qrcode"),
      //   pyotpUri,
      //   function (error) {
      //     if (error) console.error(error);
      //   },
      // );
    }
  }
</script>

<section class="section is-large">
  LOL
  <div class="box">
    <h2 class="title">Your TOTP configuration:</h2>
    <h3 class="subtitle">
      Your account has
      {#if !has_active_otp}
        not
      {/if}
      configured TOTP
    </h3>
    <button class="button is-primary" on:click={generateTOTPSecret}>
      <span class="icon is-small">
        <i class="fas fa-bold fa-arrows-rotate fa-solid"></i>
      </span>
      <span>Generate new TOTP secret</span>
    </button>
    {#if pyotpUri !== ""}
      <canvas id="qrcode"></canvas>
    {/if}
  </div>
</section>
