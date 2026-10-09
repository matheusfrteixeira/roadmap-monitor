<template>
  <div v-if="timetrackerStore.isTimerRunning" class="timer-bar">
    <div class="timer-info">
      <span class="pulse-indicator">●</span>
      <strong>Cronometrando:</strong>
      <span class="activity-tag">{{ timetrackerStore.activeTimer?.activityName }}</span>
      <span class="timer-display">{{ timetrackerStore.formattedTimer }}</span>
    </div>
    <div class="timer-actions">
      <button class="btn pink" @click="showStopModal = true">
        ⏹️ Parar & Gravar
      </button>
    </div>

    <!-- Modal para descrição do apontamento -->
    <div v-if="showStopModal" class="modal-backdrop" @click.self="showStopModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Salvar Apontamento de Horas</h2>
          <button class="modal-close" @click="showStopModal = false">×</button>
        </div>
        <div>
          <p style="margin: 0 0 8px; font-size: 0.82rem; color: var(--muted)">
            Atividade: <strong>{{ timetrackerStore.activeTimer?.activityName }}</strong><br>
            Tempo decorrido: <strong>{{ timetrackerStore.formattedTimer }}</strong>
          </p>
          <div class="form-group">
            <label>O que você realizou nesta sessão?</label>
            <textarea
              v-model="notes"
              class="form-control"
              placeholder="Descreva as tarefas concluídas, impedimentos ou notas gerais..."
            ></textarea>
          </div>
          <div style="display:flex; justify-content: flex-end; gap: 8px; margin-top: 12px;">
            <button class="btn secondary" @click="showStopModal = false">Continuar Cronômetro</button>
            <button class="btn pink" :disabled="saving" @click="confirmStop">
              {{ saving ? 'Gravando...' : 'Confirmar & Gravar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useTimetrackerStore } from '@/stores/timetracker'

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
  } catch (err) {
    alert('Erro ao salvar apontamento. Verifique a conexão com a API.')
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
  margin-top: 8px;
  animation: fadeIn 0.3s ease;
}

.timer-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.84rem;
  color: var(--text);
}

.pulse-indicator {
  color: var(--pink);
  font-size: 0.85rem;
  animation: pulse 1s infinite;
}

.activity-tag {
  background: #fff;
  border: 1px solid #FBCFE8;
  padding: 2px 7px;
  border-radius: 5px;
  font-size: 0.82rem;
  color: var(--purple);
  font-weight: 700;
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.timer-display {
  font-family: monospace;
  font-size: 0.9rem;
  font-weight: 800;
  color: var(--pink);
  background: #fff;
  padding: 2px 7px;
  border-radius: 5px;
  border: 1px solid #FBCFE8;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.3; }
  100% { opacity: 1; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

