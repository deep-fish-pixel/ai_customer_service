<script lang="ts">
  import Snackbar, { Actions, Label } from '@smui/snackbar';
  import IconButton from '@smui/icon-button';
  import {injectToast} from "../utils/toast";

  let snackbarWithClose: Snackbar;
  let message = '';

  injectToast((msg: string) => {
    message = msg;
    snackbarWithClose.open();
  });

</script>

<Snackbar bind:this={snackbarWithClose}>
  <Label>{message}</Label>
  <Actions>
    <IconButton class="material-icons" title="Dismiss"></IconButton>
  </Actions>
</Snackbar>

<style lang="scss">

</style>