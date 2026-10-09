<template>
  <div v-if="timetrackerStore.isTimerRunning" class="timer-bar">
    <div class="timer-info">
      <span class="pulse-indicator">●</span>
      <strong>Cronometrando:</strong>
      <span class="activity-tag">{{ timetrackerStore.activeTimer?.activityName }}</span>
      <span class="timer-display">{{ timetrackerStore.formattedTimer }}</span>
    </div>
    <div class="timer-actions">
      <Button
        label="Parar & Gravar"
        icon="pi pi-stop-circle"
        severity="danger"
        size="small"
        @click="showStopModal = true"
      />
    </div>

    <!-- Dialog do PrimeVue para descrição do apontamento -->
    <Dialog
      v-model:visible="showStopModal"
      modal
      header="Salvar Apontamento de Horas"
      :style="{ width: '480px' }"
    >
      <div style="display:flex; flex-direction:column; gap:10px; margin-top:6px;">
        <div style="background:var(--purple4); border:1px solid var(--line); border-radius:8px; padding:10px;">
          <div style="font-size:0.86rem; color:var(--muted);">
            Atividade: <strong style="color:var(--purple)">{{ timetrackerStore.activeTimer?.activityName }}</strong>
          </div>
          <div style="font-size:0.86rem; color:var(--muted); margin-top:2px;">
            Tempo decorrido: <strong style="color:var(--pink)">{{ timetrackerStore.formattedTimer }}</strong>
          </div>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.84rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">
            O que você realizou nesta sessão?
          </label>
          <Textarea
            v-model="notes"
            rows="4"
            placeholder="Descreva as entregas concluídas, impedimentos ou notas gerais..."
            style="width:100%; resize:vertical; font-size:0.9rem;"
          />
        </div>
      </div>

      <template #footer>
        <Button
          label="Continuar Cronômetro"
          severity="secondary"
          text
          @click="showStopModal = false"
        />
        <Button
          label="Confirmar & Gravar"
          icon="pi pi-check"
          severity="danger"
          :loading="saving"
          @click="confirmStop"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useTimetrackerStore } from '@/stores/timetracker'

import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import Textarea from 'primevue/textarea'

const toast = useToast()
const timetrackerStore = useTimetrackerStore()
const showStopModal = ref(false)
const notes = ref('')
const saving = ref(false)

async function confirmStop() {
  saving.value = true
  try {
    await timetrackerStore.stopTimer(notes.value)
    notes.value = ''
    showStopModal.value = false
    toast.add({
      severity: 'success',
      summary: 'Apontamento Gravado',
      detail: 'Seu tempo e observações foram registrados com sucesso!',
      life: 3500
    })
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: 'Erro ao salvar apontamento. Verifique a conexão com a API.',
      life: 4000
    })
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.timer-bar {
  background: #FFF0F5;
  border: 1px solid #FBCFE8;
  border-radius: 10px;
  padding: 6px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(237, 30, 129, 0.08);
  margin-bottom: 8px;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.timer-info {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.95rem;
  color: var(--text);
}

.pulse-indicator {
  color: var(--pink);
  font-size: 1.2rem;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
  100% { opacity: 1; transform: scale(1); }
}

.activity-tag {
  background: #fff;
  border: 1px solid #FBCFE8;
  color: var(--pink);
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  max-width: 280px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.timer-display {
  font-family: 'Courier New', Courier, monospace;
  font-weight: 800;
  font-size: 1.15rem;
  color: #1F192C;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid #F8B4D9;
  padding: 2px 8px;
  border-radius: 6px;
}

.timer-actions {
  display: flex;
  gap: 6px;
}
</style>
