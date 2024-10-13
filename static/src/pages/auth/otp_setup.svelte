<script>
  import * as QRCode from "qrcode";
  export let messages;
  export let errors;
  export let has_active_otp;

  let successMessage = "";
  let errorMessage = "";
  let pyotpUri = "";
  let currentUser = null;
  let otp = "";

  async function generateTOTPSecret() {
    const response = await fetch("/auth/otp");
    const responseJson = await response.json();
    if (response.status === 200) {
      currentUser = responseJson;
      pyotpUri = currentUser.pyotp_uri;
      QRCode.toCanvas(
        document.getElementById("qrcode"),
        pyotpUri,
        function (error) {
          if (error) console.error(error);
        },
      );
    }
  }

  async function copyPyotpUri() {
    await navigator.clipboard.writeText(pyotpUri);
  }

  async function savePyotpSecret() {
    const response = await fetch(`/auth/otp/setup/${otp}`, {
      method: "POST",
      body: JSON.stringify(currentUser),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.status === 200) {
      successMessage = "Your TOTP was configured successfully!";
      setTimeout(() => {
        successMessage = "";
      }, 5000);
    } else {
      errorMessage = "invalid OTP";
    }
  }
</script>

<section class="section is-large">
  {#if successMessage !== ""}
    <div class="notification is-success is-light">
      <button class="delete" on:click={() => (successMessage = "")}></button>
      {successMessage}
    </div>
  {/if}
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
    <figure class="image is-square qrcode">
      <canvas id="qrcode" on:click={copyPyotpUri}></canvas>
    </figure>
    {#if pyotpUri !== ""}
      <form action="" on:submit|preventDefault={savePyotpSecret}>
        <div class="field">
          <label class="label" for="name">OTP</label>
          <div class="control">
            <input
              id="name"
              class="input"
              type="text"
              minlength="6"
              maxlength="6"
              placeholder="123456"
              required
              bind:value={otp}
            />
          </div>
          {#if errorMessage !== ""}
            <p class="help is-danger">{errorMessage}</p>
          {/if}
        </div>
        <div class="control">
          <button class="button is-link">Save TOTP Secret</button>
        </div>
      </form>
    {/if}
  </div>
</section>

<style>
  .qrcode {
    width: 196px;
    height: 196px;
  }

  #qrcode:hover {
    cursor: pointer;
  }
</style>
