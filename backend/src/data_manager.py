#!/usr/bin/env python3
"""
Data Management Module for Academic Burnout Detection System

This module handles data export, backup, and management operations.
"""

import pandas as pd
import json
import os
from datetime import datetime
import shutil
from pathlib import Path


def export_student_data():
    """Export student data to CSV format."""
    try:
        # Load the main dataset
        data_path = os.path.join('data', 'student_data.csv')
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            
            # Add timestamp to filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = os.path.join('exports', f'student_data_export_{timestamp}.csv')
            
            # Create exports directory
            os.makedirs('exports', exist_ok=True)
            
            # Save the data
            df.to_csv(export_path, index=False)
            
            return {
                'success': True,
                'file_path': export_path,
                'records': len(df),
                'message': f'Successfully exported {len(df)} student records'
            }
        else:
            return {
                'success': False,
                'error': 'Student data file not found'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def export_student_results():
    """Export student calculation results to CSV format."""
    try:
        results_path = os.path.join('data', 'student_results.csv')
        if os.path.exists(results_path):
            df = pd.read_csv(results_path)
            
            # Add timestamp to filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = os.path.join('exports', f'student_results_export_{timestamp}.csv')
            
            # Create exports directory
            os.makedirs('exports', exist_ok=True)
            
            # Save the data
            df.to_csv(export_path, index=False)
            
            return {
                'success': True,
                'file_path': export_path,
                'records': len(df),
                'message': f'Successfully exported {len(df)} calculation results'
            }
        else:
            return {
                'success': False,
                'error': 'Student results file not found'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def create_system_backup():
    """Create a complete system backup."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join('backups', f'system_backup_{timestamp}')
        
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Files and directories to backup
        backup_items = {
            'data': 'data',
            'reports': 'reports', 
            'exports': 'exports',
            'static/charts': 'static/charts',
            'static/graphs': 'static/graphs'
        }
        
        backed_up_items = []
        
        for backup_name, source_path in backup_items.items():
            if os.path.exists(source_path):
                dest_path = os.path.join(backup_dir, backup_name)
                
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(source_path, dest_path)
                
                backed_up_items.append(backup_name)
        
        # Create backup metadata
        metadata = {
            'backup_timestamp': timestamp,
            'backup_date': datetime.now().isoformat(),
            'items_backed_up': backed_up_items,
            'total_items': len(backed_up_items)
        }
        
        metadata_path = os.path.join(backup_dir, 'backup_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            'success': True,
            'backup_path': backup_dir,
            'items_backed_up': backed_up_items,
            'message': f'Successfully backed up {len(backed_up_items)} system components'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_system_statistics():
    """Get comprehensive system statistics."""
    try:
        stats = {}
        
        # Student data statistics
        data_path = os.path.join('data', 'student_data.csv')
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            stats['student_data'] = {
                'total_records': len(df),
                'last_updated': datetime.fromtimestamp(os.path.getmtime(data_path)).isoformat(),
                'file_size': os.path.getsize(data_path)
            }
        else:
            stats['student_data'] = {'status': 'File not found'}
        
        # Student results statistics
        results_path = os.path.join('data', 'student_results.csv')
        if os.path.exists(results_path):
            df = pd.read_csv(results_path)
            stats['student_results'] = {
                'total_calculations': len(df),
                'last_updated': datetime.fromtimestamp(os.path.getmtime(results_path)).isoformat(),
                'file_size': os.path.getsize(results_path)
            }
        else:
            stats['student_results'] = {'status': 'File not found'}
        
        # Reports statistics
        reports_dir = 'reports'
        if os.path.exists(reports_dir):
            report_files = [f for f in os.listdir(reports_dir) if f.endswith('.txt')]
            stats['reports'] = {
                'total_reports': len(report_files),
                'last_updated': datetime.fromtimestamp(os.path.getmtime(reports_dir)).isoformat() if report_files else None
            }
        else:
            stats['reports'] = {'status': 'Directory not found'}
        
        # Charts statistics
        charts_dir = os.path.join('static', 'charts')
        if os.path.exists(charts_dir):
            chart_files = [f for f in os.listdir(charts_dir) if f.endswith('.png')]
            stats['charts'] = {
                'total_charts': len(chart_files),
                'chart_files': chart_files
            }
        else:
            stats['charts'] = {'status': 'Directory not found'}
        
        return {
            'success': True,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def cleanup_old_files(days_old=30):
    """Clean up old export and backup files."""
    try:
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        cleaned_files = []
        
        # Clean up old exports
        exports_dir = 'exports'
        if os.path.exists(exports_dir):
            for file in os.listdir(exports_dir):
                file_path = os.path.join(exports_dir, file)
                if os.path.getmtime(file_path) < cutoff_time:
                    os.remove(file_path)
                    cleaned_files.append(file)
        
        # Clean up old backups (only remove empty directories)
        backups_dir = 'backups'
        if os.path.exists(backups_dir):
            for item in os.listdir(backups_dir):
                item_path = os.path.join(backups_dir, item)
                if os.path.isdir(item_path) and os.path.getmtime(item_path) < cutoff_time:
                    try:
                        shutil.rmtree(item_path)
                        cleaned_files.append(item)
                    except:
                        pass  # Directory not empty, skip
        
        return {
            'success': True,
            'cleaned_files': len(cleaned_files),
            'message': f'Cleaned up {len(cleaned_files)} old files'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
