import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ChatMessage {
  sender: 'user' | 'urbania';
  message: string;
  timestamp: Date;
}

@Component({
  selector: 'app-urbania',
  imports: [CommonModule, FormsModule],
  templateUrl: './urbania.html',
  styleUrl: './urbania.scss'
})
export class UrbaniaComponent {
  isOpen = false;
  isMinimized = false;
  currentMessage = '';
  messages: ChatMessage[] = [
    {
      sender: 'urbania',
      message: '¡Hola! Soy UrbanIA, tu asistente para el reciclaje urbano. ¿En qué puedo ayudarte hoy? 🌱',
      timestamp: new Date()
    }
  ];

  predefinedQuestions = [
    '¿Cómo reportar material?',
    '¿Qué tipos de material acepta?',
    '¿Cuánto tiempo tarda la recolección?',
    '¿Cómo ser reciclador?'
  ];

  toggleChat() {
    this.isOpen = !this.isOpen;
    this.isMinimized = false;
  }

  minimizeChat() {
    this.isMinimized = true;
  }

  maximizeChat() {
    this.isMinimized = false;
  }

  closeChat() {
    this.isOpen = false;
    this.isMinimized = false;
  }

  sendMessage() {
    if (this.currentMessage.trim()) {
      // Agregar mensaje del usuario
      this.messages.push({
        sender: 'user',
        message: this.currentMessage,
        timestamp: new Date()
      });

      // Simular respuesta de UrbanIA
      setTimeout(() => {
        this.messages.push({
          sender: 'urbania',
          message: this.getUrbanIAResponse(this.currentMessage),
          timestamp: new Date()
        });
      }, 1000);

      this.currentMessage = '';
    }
  }

  sendPredefinedQuestion(question: string) {
    this.currentMessage = question;
    this.sendMessage();
  }

  private getUrbanIAResponse(userMessage: string): string {
    const message = userMessage.toLowerCase();
    
    if (message.includes('reportar') || message.includes('reporte')) {
      return '¡Perfecto! Para reportar material reciclable, ve a "Reportar material" en el menú principal. Necesitarás indicar el tipo de material, ubicación y peso aproximado. ¿Te ayudo con algo más? 📦';
    }
    
    if (message.includes('tipo') || message.includes('material')) {
      return 'Aceptamos varios tipos de materiales: Plástico (botellas, envases), Papel y cartón, Vidrio (botellas, frascos), Metal (latas, envases). ¡Cada material cuenta para el medio ambiente! ♻️';
    }
    
    if (message.includes('tiempo') || message.includes('recolección')) {
      return 'El tiempo de recolección varía según la zona, pero generalmente es de 24-48 horas. Te notificaremos cuando un reciclador acepte tu reporte y esté en camino. ⏰';
    }
    
    if (message.includes('reciclador') || message.includes('ser reciclador')) {
      return 'Para ser reciclador, regístrate seleccionando "Reciclador" en el registro. Podrás ver reportes cercanos, aceptar rutas y ayudar a tu comunidad mientras generas ingresos. 🚴‍♂️';
    }
    
    if (message.includes('co2') || message.includes('impacto')) {
      return 'Cada kilogramo de material reciclado evita aproximadamente 0.5-2 kg de CO₂. ¡Tu contribución es valiosa para el planeta! 🌍';
    }
    
    return 'Gracias por tu pregunta. Estoy aquí para ayudarte con el reciclaje urbano. Puedes preguntarme sobre reportes, tipos de materiales, tiempos de recolección o cómo ser reciclador. 🤖';
  }
}