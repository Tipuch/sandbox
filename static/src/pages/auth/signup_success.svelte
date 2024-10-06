<script>
  export let messages;
  export let errors;
  export let current_user;
  export let activation_link;
  export let confirmed;

  async function activateAccount() {
    const response = await fetch(activation_link, {
      method: "GET",
    });
    const response_json = await response.json();
    if (response.status === 200 && response_json.confirmed_at !== null) {
      current_user = response_json;
      confirmed = true;
    }
  }
</script>

<section class="section is-large">
  <div class="box">
    <h2 class="title">your activation link is:</h2>
    <h3 class="subtitle">{activation_link}</h3>
    <h3 class="subtitle">
      Your account is
      {#if !confirmed}
        not
      {/if}
      confirmed
    </h3>
    <button
      class="button is-secondary"
      on:click={() => {
        document.location = "/auth/signup/success";
      }}
    >
      <span class="icon is-small">
        <i class="fas fa-bold fa-arrows-rotate fa-solid"></i>
      </span>
      <span>Refresh the token</span>
    </button>

    <button class="button is-primary" on:click={activateAccount}>
      <span class="icon is-small">
        <i class="fas fa-bold fa-arrow-right fa-solid"></i>
      </span>
      <span>Activate account</span>
    </button>
  </div>
</section>
