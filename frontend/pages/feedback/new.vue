<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-3xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Submit Feedback</h1>
        <p class="mt-2 text-gray-600">
          Share your ideas, report bugs, or suggest improvements
        </p>
      </div>

      <div class="bg-white shadow rounded-lg">
        <form @submit.prevent="submitFeedback" class="p-6 space-y-6">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700">
              Title <span class="text-red-500">*</span>
            </label>
            <input
              id="title"
              v-model="form.title"
              type="text"
              required
              class="mt-1 input"
              placeholder="Brief description of your feedback"
            >
          </div>

          <div>
            <label for="type" class="block text-sm font-medium text-gray-700">
              Type <span class="text-red-500">*</span>
            </label>
            <select id="type" v-model="form.type" required class="mt-1 input">
              <option value="">Select feedback type</option>
              <option value="bug">Bug Report</option>
              <option value="feature">Feature Request</option>
              <option value="improvement">Improvement</option>
              <option value="general">General Feedback</option>
            </select>
          </div>

          <div>
            <label for="priority" class="block text-sm font-medium text-gray-700">
              Priority
            </label>
            <select id="priority" v-model="form.priority" class="mt-1 input">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>

          <div>
            <label for="description" class="block text-sm font-medium text-gray-700">
              Description <span class="text-red-500">*</span>
            </label>
            <textarea
              id="description"
              v-model="form.description"
              rows="6"
              required
              class="mt-1 input"
              placeholder="Provide detailed information about your feedback..."
            ></textarea>
            <p class="mt-2 text-sm text-gray-500">
              {{ form.description.length }}/1000 characters
            </p>
          </div>

          <!-- Bug Report Specific Fields -->
          <div v-if="form.type === 'bug'" class="space-y-4 p-4 bg-red-50 rounded-lg">
            <h3 class="text-lg font-medium text-red-900">Bug Report Details</h3>
            
            <div>
              <label for="steps" class="block text-sm font-medium text-red-700">
                Steps to Reproduce
              </label>
              <textarea
                id="steps"
                v-model="form.stepsToReproduce"
                rows="3"
                class="mt-1 input"
                placeholder="1. Go to...&#10;2. Click on...&#10;3. See error"
              ></textarea>
            </div>

            <div>
              <label for="expected" class="block text-sm font-medium text-red-700">
                Expected Behavior
              </label>
              <textarea
                id="expected"
                v-model="form.expectedBehavior"
                rows="2"
                class="mt-1 input"
                placeholder="What should have happened?"
              ></textarea>
            </div>

            <div>
              <label for="actual" class="block text-sm font-medium text-red-700">
                Actual Behavior
              </label>
              <textarea
                id="actual"
                v-model="form.actualBehavior"
                rows="2"
                class="mt-1 input"
                placeholder="What actually happened?"
              ></textarea>
            </div>

            <div>
              <label for="environment" class="block text-sm font-medium text-red-700">
                Environment
              </label>
              <input
                id="environment"
                v-model="form.environment"
                type="text"
                class="mt-1 input"
                :placeholder="defaultEnvironment"
              >
            </div>
          </div>

          <!-- Feature Request Specific Fields -->
          <div v-if="form.type === 'feature'" class="space-y-4 p-4 bg-blue-50 rounded-lg">
            <h3 class="text-lg font-medium text-blue-900">Feature Request Details</h3>
            
            <div>
              <label for="business-case" class="block text-sm font-medium text-blue-700">
                Business Justification
              </label>
              <textarea
                id="business-case"
                v-model="form.businessJustification"
                rows="3"
                class="mt-1 input"
                placeholder="Why is this feature important? What problem does it solve?"
              ></textarea>
            </div>

            <div>
              <label for="proposed-solution" class="block text-sm font-medium text-blue-700">
                Proposed Solution
              </label>
              <textarea
                id="proposed-solution"
                v-model="form.proposedSolution"
                rows="3"
                class="mt-1 input"
                placeholder="How would you like this feature to work?"
              ></textarea>
            </div>
          </div>

          <div class="flex items-center">
            <input
              id="is-public"
              v-model="form.isPublic"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            >
            <label for="is-public" class="ml-2 block text-sm text-gray-900">
              Make this feedback public (others can see and vote on it)
            </label>
          </div>

          <div v-if="error" class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  Error submitting feedback
                </h3>
                <div class="mt-2 text-sm text-red-700">
                  {{ error }}
                </div>
              </div>
            </div>
          </div>

          <div class="flex items-center justify-between pt-6 border-t border-gray-200">
            <NuxtLink
              to="/feedback"
              class="btn btn-secondary"
            >
              Cancel
            </NuxtLink>
            <button
              type="submit"
              :disabled="loading || !isFormValid"
              class="btn btn-primary"
            >
              <span v-if="loading">Submitting...</span>
              <span v-else>Submit Feedback</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const api = useApi()
const router = useRouter()

const form = reactive({
  title: '',
  type: '',
  priority: 'medium',
  description: '',
  isPublic: true,
  // Bug report fields
  stepsToReproduce: '',
  expectedBehavior: '',
  actualBehavior: '',
  environment: '',
  // Feature request fields
  businessJustification: '',
  proposedSolution: ''
})

const error = ref('')
const loading = ref(false)

const isFormValid = computed(() => {
  return form.title.trim() && 
         form.type && 
         form.description.trim() && 
         form.description.length <= 1000
})

// Auto-detect environment for bug reports
const defaultEnvironment = computed(() => {
  if (process.client) {
    return `${navigator.platform} - ${navigator.userAgent}`
  }
  return 'Unknown environment'
})

// Set default environment when bug type is selected
watch(() => form.type, (newType) => {
  if (newType === 'bug' && !form.environment) {
    form.environment = defaultEnvironment.value
  }
})

const submitFeedback = async () => {
  if (!isFormValid.value) return
  
  error.value = ''
  loading.value = true
  
  try {
    // Build the payload
    const payload: any = {
      title: form.title.trim(),
      description: form.description.trim(),
      type: form.type,
      priority: form.priority,
      is_public: form.isPublic
    }

    // Add type-specific fields to description
    if (form.type === 'bug') {
      let bugDetails = form.description.trim()
      if (form.stepsToReproduce) {
        bugDetails += `\n\n**Steps to Reproduce:**\n${form.stepsToReproduce}`
      }
      if (form.expectedBehavior) {
        bugDetails += `\n\n**Expected Behavior:**\n${form.expectedBehavior}`
      }
      if (form.actualBehavior) {
        bugDetails += `\n\n**Actual Behavior:**\n${form.actualBehavior}`
      }
      if (form.environment) {
        bugDetails += `\n\n**Environment:**\n${form.environment}`
      }
      payload.description = bugDetails
    } else if (form.type === 'feature') {
      let featureDetails = form.description.trim()
      if (form.businessJustification) {
        featureDetails += `\n\n**Business Justification:**\n${form.businessJustification}`
      }
      if (form.proposedSolution) {
        featureDetails += `\n\n**Proposed Solution:**\n${form.proposedSolution}`
      }
      payload.description = featureDetails
    }
    
    const response = await api('/feedback', {
      method: 'POST',
      body: payload
    })
    
    // Redirect to the new feedback
    await router.push(`/feedback/${response.id}`)
  } catch (e: any) {
    error.value = e.data?.message || 'Failed to submit feedback'
  } finally {
    loading.value = false
  }
}

useHead({
  title: 'Submit Feedback - Feedback Hub',
  meta: [
    { name: 'description', content: 'Share your ideas and report issues' }
  ]
})
</script>