/*
 * Copyright (c) 1995, 2008, Oracle and/or its affiliates. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *   - Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *
 *   - Neither the name of Oracle or the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */ 

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;

import javax.swing.BorderFactory;
import javax.swing.JColorChooser;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.colorchooser.AbstractColorChooserPanel;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

/* ColorChooserDemo.java requires no other files. */
public class ColorChooserDemo extends JPanel
                              implements ChangeListener {

    /**
	 * 
	 */
	private static final long serialVersionUID = -4830641426666246099L;
	protected JColorChooser tcc;
    protected JLabel banner;
    protected JLabel preview;
    protected String nota;

    public ColorChooserDemo() {
        super(new BorderLayout());

        //Set up the banner at the top of the window
        banner = new JLabel();
        nota = new String();

        JPanel bannerPanel = new JPanel(new BorderLayout());
        //bannerPanel.add(banner, BorderLayout.CENTER);
        bannerPanel.setBorder(BorderFactory.createEmptyBorder());

        //Set up color chooser for setting text color
        tcc = new JColorChooser(banner.getForeground());
        
        AbstractColorChooserPanel[] oldPanels = tcc.getChooserPanels();
        
        for(int i=0; i<oldPanels.length; i++){
        	if(i != 1 && i != 3){
        		tcc.removeChooserPanel(oldPanels[i]);
        	}	
        }
       
        tcc.getSelectionModel().addChangeListener(this);
        tcc.setBorder(BorderFactory.createTitledBorder(
                                             "Escolha a cor"));
        
        preview = new JLabel("Nota", JLabel.CENTER);
        preview.setFont(new Font("Serif", Font.BOLD | Font.ITALIC, 48));
        preview.setSize(preview.getPreferredSize());
        preview.setBorder(BorderFactory.createTitledBorder("Nota"));
        
        tcc.setPreviewPanel(preview);      
        
        add(bannerPanel, BorderLayout.CENTER);
        add(tcc, BorderLayout.PAGE_END);

    }

    public void stateChanged(ChangeEvent e) {
        Color newColor = tcc.getColor();
        
        defineNota(newColor);
    }
    
    public void defineNota(Color c){
    	
    	float[] hsbvals = Color.RGBtoHSB(c.getRed(), c.getGreen(), c.getBlue(), null);
        
        int h = (int) (hsbvals[0] * 360);
        int s = (int) (hsbvals[1] * 100);
        int v = (int) (hsbvals[2] * 100);
        
        System.out.println("H: " + h + "\nS: " + s + "\nV: " + v);
        
        //Define branco e cinzas
        if(s <= 9){
        	
        	if(v >= 90){
        		nota = "C8";
        	}
        	else if(v >= 63){
        		nota = "B0";
        	}
        	else if(v >= 35){
        		nota = "A#0";
        	}
        	else{
        		nota = "A0";
        	}
        	
        }else{
        	
        	//Define preto
        	if(v < 35){
        		nota = "A0";
        	}else{
        		//Define o resto das cores
        		if(h > 330 || h <= 8){
                	nota = "A";
                }
                else if(h <= 27){
                	nota = "A#";
                }
                else if(h <= 65){
                	nota = "B";
                }
                else if(h <= 103){
                	nota = "C";
                }
                else if(h <= 122){
                	nota = "C#";
                }
                else if(h <= 160){
                	nota = "D";
                }
                else if(h <= 179){
                	nota = "D#";
                }
                else if(h <= 217){
                	nota = "E";
                }
                else if(h <= 255){
                	nota = "F";
                }
                else if(h <= 274){
                	nota = "F#";
                }
                else if(h <= 312){
                	nota = "G";
                }
                else{
                	nota = "G#";
                }
        		
        		defineEscala(s);

        	}
        }
        
        //defineIntervaloRGB();
        
        preview.setText(nota);
        System.out.println("Nota: " + nota);
    }
   
    public void defineIntervaloRGB(){
    	
    	for(int s=0; s<=100; s++){
    		for(int v = 0; v<= 100; v++){
    			for(int h = 0; h <= 360; h++){
    		        
    		        //Define o resto das cores
    		        if(h > 330 || h <= 8){
    		        	nota = "A";
    		        	
    		        	int rgb = Color.HSBtoRGB(h, s, v);
    		        	System.out.println(rgb);
    		        }
    		        else if(h <= 27){
    		            nota = "A#";
    		        }
    		        else if(h <= 65){
    		            nota = "B";
    		        }
    		        else if(h <= 103){
    		            nota = "C";
    		        }
    		        else if(h <= 122){
    		            nota = "C#";
    		        }
    		        else if(h <= 160){
    		            nota = "D";
    		        }
    		        else if(h <= 179){
    		            nota = "D#";
    		        }
    		        else if(h <= 217){
    		            nota = "E";
    		        }
    		        else if(h <= 255){
    		            nota = "F";
    		        }
    		        else if(h <= 274){
    		            nota = "F#";
    		        }
    		        else if(h <= 312){
    		          	nota = "G";
    		        }
    		        else{
    		            nota = "G#";
    		        }        
    		    }
    		        
    	    }
    		
    	}
    
    }
    
    public void defineEscala(int s){
    	
    	if(s <= 22){
    		nota += "7";
    	}
    	else if(s <= 35){
    		nota += "6";
    	}
    	else if(s <= 48){
    		nota += "5";
    	}
    	else if(s <= 61){
    		nota += "4";
    	}
    	else if(s <= 74){
    		nota += "3";
    	}
    	else if(s <= 87){
    		nota += "2";
    	}
    	else if(s <= 100){
    		nota += "1";
    	}
    }

    /**
     * Create the GUI and show it.  For thread safety,
     * this method should be invoked from the
     * event-dispatching thread.
     */
    private static void createAndShowGUI() {
        //Create and set up the window.
        JFrame frame = new JFrame("Algoritmo Cor-Som");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        //Create and set up the content pane.
        JComponent newContentPane = new ColorChooserDemo();
        newContentPane.setOpaque(true); //content panes must be opaque
        frame.setContentPane(newContentPane);

        //Display the window.
        frame.pack();
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        //Schedule a job for the event-dispatching thread:
        //creating and showing this application's GUI.
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                createAndShowGUI();
            }
        });
    }
}