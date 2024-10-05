<script>
  export let messages;
  export let errors;
  export let current_user;
  export let activation_link;
</script>

<section class="section is-large">
  <h2 class="subtitle">your activation link is "{activation_link}"</h2>
  <button
    class="button is-primary"
    on:click={() => {
      document.location = "/auth/signup/success";
    }}
  >
    <span class="icon is-small">
      <i class="fas fa-bold fa-arrows-rotate fa-solid"></i>
    </span>
    <span>Refresh the token</span>
  </button>
</section>
